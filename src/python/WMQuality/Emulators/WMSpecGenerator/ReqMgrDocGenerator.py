from __future__ import (print_function, division)
import time
import random

NUM_OF_REQUEST = 1
ITERATIONS =1
NUM_OF_JOBS_PER_REQUEST = 11

def generate_reqmgr_schema(number=NUM_OF_REQUEST):
    """
    generate the request with following structure
    doc["_id"] = schema['RequestName']
    doc["workflow"] = schema['RequestName']
    doc["requestor"] = schema['Requestor']
    doc["campaign"] = schema['Campaign']
    doc["request_type"] = schema['RequestType']
    doc["priority"] = schema['RequestPriority']
    doc["group"] = schema['Group']
    doc["request_date"] = schema['RequestDate']
    doc["type"] = "reqmgr_request"
    # additional field
    doc["inputdataset"] = schema.get('InputDataset', "")
    # additional field for Analysis work
    doc["vo_group"] = schema.get('VoGroup', "")
    doc["vo_role"] = schema.get('VoRole', "")
    doc["user_dn"] = schema.get('RequestorDN', "")
    doc["async_dest"] = schema.get('asyncDest', "")
    doc["dbs_url"] = schema.get("DbsUrl", "")
    doc["publish_dbs_url"] = schema.get("PublishDbsUrl", "")
    # team name is not yet available need to be updated in assign status
    #doc['team'] = schema['team']
    """
    docs = []
    for i in xrange(number):
        doc = {"RequestName": "test_workflow_%s" % i,
               "InputDataset": "/Photon/Run2011A-v1/RAW",
               "Group": "cmsdataops",
               "RequestDate": [2012, 1, 11, 17, 49, 50],
               "Campaign": "SryuTest-%s" % (i % 5),
               "RequestPriority": "1",
               "Requestor": "cmsdataops",
               "RequestType": "ReReco"
               #"site_white_list": ["T1_DE_KIT"],
               #"team": "cmsdataops"
                }
        docs.append(doc)
    return docs


def generate_reqmgr_requests(number=NUM_OF_REQUEST):
    """
    generate the request with following structure
      {
       "_id": "cmsdataops_sryu_test4_120111_114950_128",
       "_rev": "6-02b17b4eabcf333e7499c0fa0ae5055b",
       "inputdataset": "/Photon/Run2011A-v1/RAW",
       "group": "cmsdataops",
       "request_date": [2012, 1, 11, 17, 49, 50],
       "campaign": "SryuTest2",
       "workflow": "cmsdataops_sryu_test4_120111_114950_128",
       "priority": "1",
       "requestor": "cmsdataops",
       "request_type": "ReReco",
       "type": "reqmgr_request",
       "request_status": [
           {
               "status": "new",
               "update_time": 1326304190
           },
           {
               "status": "assignment-approved",
               "update_time": 1326304216
           },
           {
               "status": "assigned",
               "update_time": 1326304227
           }
       ],
       "site_white_list": [
           "T1_DE_KIT"
       ],
       "team": "cmsdataops"
    }
    """
    docs = []
    for i in xrange(number):
        doc = {"_id": "test_workflow_%s" % i,
               "inputdataset": "/Photon/Run2011A-v1/RAW",
               "group": "cmsdataops",
               "request_date": [2012, 1, 11, 17, 49, 50],
               "campaign": "SryuTest-%s" % (i % 5),
               "workflow": "test_workflow_%s" % i,
               "priority": "1",
               "requestor": "cmsdataops",
               "request_type": "ReReco",
               "type": "reqmgr_request",
               "request_status": [
                                  {"status": "new", "update_time": 1326304190},
                                  {"status": "assignment-approved", "update_time": 1326304216},
                                  {"status": "assigned", "update_time": 1326304227}
                                 ],
                "site_white_list": ["T1_DE_KIT"],
                "teams": "cmsdataops"
                }
        docs.append(doc)
    return docs


def generate_agent_requests(number=NUM_OF_REQUEST, iterations=ITERATIONS):
    """
    generate the request with following structure
      {
       "_id": "af27057919546ff8f3fc8d7f18233355",
       "_rev": "1-181021c38a5444676d7718f42ffa9a89",
       "status": {
           "inWMBS": 1,
           "queued": {
               "retry": 1
           }
       },
       "workflow": "cmsdataops_sryu_test4_120111_114950_128",
       "timestamp": 1326306397,
       "sites": {
           "T1_DE_KIT": {
               "queued": {
                   "retry": 1
               }
           }
       },
       "agent": "WMAgentCommissioning",
       "team": "team1,team2,cmsdataops",
       "agent_url": "cms-xen39.fnal.gov",
       "type": "agent_request"
       }
    """
    current_time = int(time.time())
    docs = []
    for cycle in xrange(iterations):
        for i in xrange(number):
            doc = {"status": {"inWMBS": 12,
                              "submitted": {"retry": 2, "running": 2, "pending": 2, "first": 2},
                              "failure": {"exception": 2, "create": 2, "submit": 2},
                              "queued": {"retry": 2, "first": 2},
                              "canceled": 2,
                              "cooloff": 2,
                              "success": 2
                             },

                "workflow": "test_workflow_%s" % i,
                "timestamp": current_time + (cycle * 10),
                "sites": {"T1_DE_KIT":
                             {
                              "submitted": {"retry": 1, "running": 1, "pending": 1, "first": 1},
                              "failure": {"exception": 1, "create": 1, "submit": 1},
                              "queued": {"retry": 1, "first": 1},
                              "canceled": 1,
                              "cooloff": 1,
                              "success": 1
                             },
                          "T1_US_FNAL":
                             {
                              "submitted": {"retry": 1, "running": 1, "pending": 1, "first": 1},
                              "failure": {"exception": 1, "create": 1, "submit": 1},
                              "queued": {"retry": 1, "first": 1},
                              "canceled": 1,
                              "cooloff": 1,
                              "success": 1
                             }
                          },
                "agent": "WMAgentCommissioning",
                "agent_teams": "team1,team2,cmsdataops",
                "agent_url": "cms-xen39.fnal.gov",
                "type": "agent_request"
            }
            docs.append(doc)
    return docs


def generate_jobsummary(request, number=NUM_OF_JOBS_PER_REQUEST):
    """
    jobSummary = {"_id": "jobid_1",  //jobid
                  "type": "jobsummary", // setvalue
                  "retrycount": job["retry_count"],
                  "workflow": workflow1, //request name
                  "task": job["task"],
                  "state": success,
                  "site": T1_US_FNAL,
                  "exitcode": 123,
                  "errors": errmsgs,
                  "lumis": inputs,
                  "output": outputs }

    errmsgs = {}
    inputs = []
    for step in fwjrDocument["fwjr"]["steps"]:
        if "errors" in fwjrDocument["fwjr"]["steps"][step]:
            errmsgs[step] = [error for error in fwjrDocument["fwjr"]["steps"][step]["errors"]]
        if "input" in fwjrDocument["fwjr"]["steps"][step] and "source" in fwjrDocument["fwjr"]["steps"][step]["input"]:
            inputs.extend( [source["runs"] for source in fwjrDocument["fwjr"]['steps'][step]["input"]["source"] if "runs" in source] )
    outputs = [ {'type': singlefile.get('module_label', None),
                 'lfn': singlefile.get('lfn', None),
                 'location': singlefile.get('locations', None),
                 'checksums': singlefile.get('checksums', {}),
                     'size': singlefile.get('size', None) } for singlefile in job["fwjr"].getAllFiles() if singlefile ]


    job status
    ['new', 'created', 'executing', 'complete', 'createfailed', 'submitfailed',
     'jobfailed', 'createcooloff',  'submitcooloff', 'jobcooloff', 'success',
     'exhausted', 'killed']
    """

    #TODO: Make more realistic
    docs = []
    statusList = ['new', 'created', 'executing', 'complete', 'createfailed', 'submitfailed',
     'jobfailed', 'createcooloff',  'submitcooloff', 'jobcooloff', 'success',
     'exhausted', 'killed']

    for i in xrange(number):
        status = statusList[random.randint(0, len(statusList)-1)]
        errmsgs = {}
        if status.find("failed"):
            exitCode = 666
            errmsgs["step1"] = {}
            errmsgs["step1"]["out"] = {}
            errmsgs["step1"]["out"]["type"] = "test error"
        else:
            exitCode = 0

        jobSummary = {"_id": "jobid_%s_%s" % (request, i),
                  "type": "jobsummary",
                  "retrycount": random.randint(0,5),
                  "workflow": request,
                  "task": "/%s/task_%s" % (request, i),
                  "state": status,
                  "site": "T1_US_FNAL",
                  "exitcode": exitCode,
                  "errors": errmsgs,
                  "lumis": [[123, 124], [567, 879]],
                  "output": [ {'type': "test-type",
                               'lfn': "/somewhere/file.root",
                               'location': ['T1_US_FNAL'],
                               'checksums': {'adler32': 'abc123', 'cksum': 'cdf123'},
                               'size': "1000" }  ]
            }
        docs.append(jobSummary)
    return docs
