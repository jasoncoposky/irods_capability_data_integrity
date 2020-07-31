__all__ = ['verify_replica_number']
from irods_capability_integrity_utils import *

def verify_replica_number(rule_args , callback, rei):

    violations = split_text_lines( rule_args[0] )
    attr = verify_replica_number_attribute

    # get a list of all matching collections given the metadata attribute

    for row0 in Query (callback, ['COLL_NAME', 'META_COLL_ATTR_VALUE'],
                       "META_COLL_ATTR_NAME = '{}'".format(attr),AS_DICT):

        number_of_replicas = int(row0['META_COLL_ATTR_VALUE'])

        coll_name = row0['COLL_NAME']

        # get a list of all data objects in the given collection
        for row1 in Query(callback,['COLL_NAME','DATA_NAME'], "COLL_NAME like '{}%'".format(coll_name)):
            matched = 0
            coll_name = row1['COLL_NAME']
            data_name = row1['DATA_NAME']

            # get all of the resource names where this objects replicas reside
            for row2 in Query(callback,['RESC_NAME'],
                              "COLL_NAME = '{}' AND DATA_NAME = '{}'".format(coll_name,data_name)):
                matched += 1
            # for resources

            if matched < number_of_replicas:
                violations.append("{0}/{1} violates the number policy: # replicas = {2}" .format(coll_name, data_name, number_of_replicas))

        # for objects

    # for collections

    rule_args[0] = join_text_lines( violations )

# verify_replica_number
