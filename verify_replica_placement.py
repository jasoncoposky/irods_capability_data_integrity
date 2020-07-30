from genquery import Query, AS_DICT

def get_error_value           ()   : return "ERROR_VALUE"
def RULE_ENGINE_CONTINUE      ()   : return 5000000
def SYS_INVALID_INPUT_PARAM   ()   : return -130000
def verify_replicas_attribute ()   : return "irods::verification::replicas"


def verify_replica_placement (rule_args, callback, rei):

    attr = verify_replicas_attribute()

    for row0 in Query (callback, ['COLL_NAME','META_COLL_ATTR_VALUE'],
                       "META_COLL_ATTR_NAME = '{}'".format(attr), AS_DICT):

        resource_list = row0 ['META_COLL_ATTR_VALUE'] 
        number_of_resources = len( resource_list.split(",") )
        coll_name = row0 ['COLL_NAME']

        for row1 in Query (callback, ['COLL_NAME','DATA_NAME'], 
                           "COLL_NAME like '{}%'".format( coll_name ), AS_DICT):
            matched = 0
            coll_name = row1['COLL_NAME']
            data_name = row1['DATA_NAME']

            for row2 in Query (callback, ['RESC_NAME'], 
                               "COLL_NAME = '{0}' AND DATA_NAME = '{1}'".format(coll_name,data_name), AS_DICT):
                resource_name = row2['RESC_NAME']
                while split_list:
                    name = split_list.pop(0).strip()
                    if name == resource_name: matched += 1

                # -- end -- for resources

            if matched < number_of_resources:
                callback.writeLine("stdout", ("Object {coll_name}/{data_name} "
                                              "violates the replica replacement policy".format(**locals()))
                                  )
        # -- end -- for objects

    # -- end -- for collections

