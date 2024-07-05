#!/usr/bin/env python

"""
_MemoryModifier_

config.RetryManager.modifiers = {50660: 'MemoryModifier'}
config.RetryManager.section_('MemoryModifier')
config.RetryManager.MemoryModifier.section_('default')
config.RetryManager.MemoryModifier.default.settings = {'requiresModify': False, 'addMemoryPerCore': 200, 'maxMemoryPerCore': 2000}
config.RetryManager.MemoryModifier.section_('Processing')
config.RetryManager.MemoryModifier.Processing.settings = {'requiresModify': True, 'addMemoryPerCore': 200, 'maxMemoryPerCore': 2500}
config.RetryManager.MemoryModifier.section_('merge')
config.RetryManager.MemoryModifier.merge.settings = {'requiresModify': True, 'multiplyMemoryPerCore': 1.2, 'maxMemoryPerCore': 3000}
"""
import time
import os
import pickle
import logging
from WMCore.WMSpec.WMTask import WMTaskHelper
from WMCore.WMSpec.WMWorkload import WMWorkloadHelper
from WMComponent.RetryManager.Modifier.BaseModifier import BaseModifier


class MemoryModifier(BaseModifier):

    def changeSandbox(self, jobPKL, newMemory):
        """
        _changeSandbox_

        Modifies the parameter maxPSS in the sandbox. This is a change that applies for all jobs in that workflow that remain to be submitted 
        """

        workload = self.getWorkload(jobPKL)
        workHelper = WMWorkloadHelper(workload)

        for task in workHelper.getAllTasks():
            
            task.setMaxPSS(newMemory)
            

        self.setWorkload(workload, jobPKL)

        return
    
    def changeMemoryForTask(self, taskPath, jobPKL, newMemory):
        """
        Approach to modify memory per task, rather than continuously changing the whole workflow
        """
        workload = self.getWorkload(jobPKL)
        workHelper = WMWorkloadHelper(workload)
        task = workHelper.getTaskByPath(taskPath)
        task.setMaxPSS(newMemory)
        self.setWorkload(workload, jobPKL)

    def changeJobPkl(self, pklFile, jobPKL, newMemory):
        """
        Modifies the pklFile job.pkl by changing the estimatedMemoryUsage to a new_memory value

        """
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
        logging.info('MemoryModifier modifying %s job pkl file. Previous value: %d. New value: %d', jobPKL['jobType'], jobPKL['estimatedMemoryUsage'], newMemory)
        os.system('echo "time: {}; job: {}; job type: {}; job old memory: {}; job new memory: {}" >> /data/tier0/WMAgent.venv3/memoryLogsChangeJobPkl.txt'.format(formatted_time, jobPKL['id'], jobPKL['jobType'], jobPKL['estimatedMemoryUsage'], newMemory))
        jobPKL['estimatedMemoryUsage'] = newMemory 
        self.savePKL(pklFile, jobPKL)

    def checkNewJobPkl(pklFile):
        with open(pklFile, 'rb') as file:
            data = pickle.load(file)
        print (data['estimatedMemoryUsage'])

    def getNewMemory(self, jobPKL, settings):
        maxMemPerCore = settings['maxMemoryPerCore']
        currentMem = jobPKL['estimatedMemoryUsage']
        currentMemPerCore = currentMem/jobPKL['numberOfCores']

        if 'multiplyMemoryPerCore' in settings:
            newMemPerCore = currentMemPerCore * settings['multiplyMemoryPerCore']
        elif 'addMemoryPerCore' in settings:
            newMemPerCore = currentMemPerCore + settings['addMemoryPerCore']
        else:
            newMemPerCore = currentMemPerCore

        if newMemPerCore > maxMemPerCore:
            newMemPerCore = maxMemPerCore
        return newMemPerCore * jobPKL['numberOfCores']
    
    def changeMemory(self, job, settings):
        """
        The "main" function in charge of modifying the memory before a retry. 
        It needs to modify the job.pkl file and the maxPSS value for the respective task
        """
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
        pklFile = '{}/job.pkl'.format(job['cache_dir']) 
        jobPKL = self.loadPKL(pklFile)

        newMemory = self.getNewMemory(jobPKL, settings)
        taskPath = self.getTaskPath(jobPKL)

        ###
        logging.info('CURRENT TASK is {}'.format(taskPath))
        logging.info('Pre-Mod dataDict: {}'.format(self.dataDict))
        ###

        if not taskPath in self.dataDict:
            self.updateDataDict(key=taskPath, value=jobPKL['estimatedMemoryUsage'])

        os.system('echo "{}; {}; {}; {}; {}" >> /data/tier0/WMAgent.venv3/srv/wmagent/2.3.4rc11/logs/jobs/{}.txt'.format(formatted_time, jobPKL['id'], jobPKL['estimatedMemoryUsage'], newMemory, jobPKL['retry_count'], jobPKL['id']))
        self.changeJobPkl(pklFile, jobPKL, newMemory)

        ###
        logging.info('Post-Mod dataDict: {}'.format(self.dataDict))
        ###

        ###
        taskMod = False
        ###

        if self.dataDict[taskPath] < newMemory:

            ###
            os.system('echo "{}; {}; {}" >> /data/tier0/WMAgent.venv3/srv/wmagent/2.3.4rc11/logs/workflows/{}.txt'.format(formatted_time, taskPath, self.dataDict[taskPath], jobPKL['workflow']))
            ###

            self.changeMemoryForTask(taskPath, jobPKL, newMemory)
            self.updateDataDict(key=taskPath, value=newMemory)

            ###
            os.system('echo "{}; {}; {}" >> /data/tier0/WMAgent.venv3/srv/wmagent/2.3.4rc11/logs/workflows/{}.txt'.format(formatted_time, taskPath, self.dataDict[taskPath], jobPKL['workflow']))
            os.system('echo "\n" >> /data/tier0/WMAgent.venv3/srv/wmagent/2.3.4rc11/logs/workflows/{}.txt'.format(jobPKL['workflow']))
            ###

            ###
            taskMod = True
            ###
        
        ###
        if taskMod:
            os.system('echo "{}; {}; {}; {}; {}" >> /data/tier0/WMAgent.venv3/srv/wmagent/2.3.4rc11/logs/jobs/{}.txt'.format(formatted_time, jobPKL['id'], jobPKL['estimatedMemoryUsage'], newMemory, jobPKL['retry_count'], taskPath, jobPKL['id']))
        ###

        logging.info('Old maxPSS: %d. New maxPSS: %d', jobPKL['estimatedMemoryUsage'], newMemory)

    def modifyJob(self, job):
        current_time = time.localtime()
        formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
        try:
            settings = self.getModifierParam(job['jobType'], 'settings')
        except:
            logging.debug('MemoryModifier did not get settings parameter for job type %s. Not modifying memory', job['jobType'])
            return

        if not 'requiresModify' in settings:
            logging.debug('MemoryModifer for job type %s does not specify requiresModify. Not modifying memory',job['jobType'])
            return 

        elif not settings['requiresModify']:
            logging.debug('MemoryModifyer for job type %s has requiresModify set to False. Not modifying memory', job['jobType'])
            return
        
        else:
            logging.info('MemoryModifier modifying memory for job %d of job type %s', job['id'], job['jobType'])
            os.system('echo "time: {}; job: {}; job type: {}" >> /data/tier0/WMAgent.venv3/memoryLogsModifyJob.txt'.format(formatted_time, job['id'], job['jobType']))
            self.changeMemory(job, settings)
