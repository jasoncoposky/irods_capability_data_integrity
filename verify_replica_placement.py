__all__ = ['verify_replica_placement']
from genquery import Query, AS_DICT
from irods_capability_integrity_utils import *


def verify_replica_placement (rule_args, callback, rei):

    violations = split_text_lines( rule_args[0] )

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
                violations.append("Object {coll_name}/{data_name} violates the replica replacement policy".format(**locals()))

        # -- end -- for objects

    # -- end -- for collections

    rule_args [0] = join_text_lines( violations )

