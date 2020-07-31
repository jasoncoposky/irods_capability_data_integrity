__all__ = ['verify_replica_checksum']
from genquery import Query, AS_DICT
from irods_capability_integrity_utils import *


def verify_replica_checksum (rule_args, callback, rei):

    (all_flag,  resource_name,  violations) = rule_args

    attr = verify_checksum_attribute()

    for row0 in Query (callback, ['COLL_NAME','META_COLL_ATTR_VALUE'],
                       "META_COLL_ATTR_NAME = '{}'".format(attr), AS_DICT):

        coll_name = row0 ['COLL_NAME']

        for row1 in Query (callback, ['COLL_NAME','DATA_NAME'], 
                           "COLL_NAME like '{}%'".format( coll_name ), AS_DICT):
            coll_name = row1['COLL_NAME']
            data_name = row1['DATA_NAME']

            if true() == all_flag:

                for row2 in Query (callback, ['DATA_REPL_NUM', 'DATA_CHECKSUM'], 
                               "COLL_NAME = '{0}' AND DATA_NAME = '{1}'".format(coll_name,data_name), AS_DICT):

                    checksum = row2['DATA_CHECKSUM']

                    retval = callback.msiDataObjChksum("{}/{}".format(coll_name,data_name), 
                                                       "forceChksum=++++replNum={0}".format(repl_num), "")
                    out = retval['arguments'][2]

                    if checksum != out: violations.append("{coll_name}/{data_name} violates the checksum policy {out} vs {checksum}".format(**locals()))
            else:
                for row2 in Query (callback, ['DATA_REPL_NUM', 'DATA_CHECKSUM'], 
                               ("COLL_NAME = '{0}' and DATA_NAME = '{1}' "
                                " and RESC_NAME = '{2}'").format(coll_name,data_name,resource_name), AS_DICT):

                    checksum = row2['DATA_CHECKSUM']

                    retval = callback.msiDataObjChksum("{}/{}".format(coll_name,data_name), 
                                                       "forceChksum=++++replNum={0}".format(repl_num), "")
                    out = retval['arguments'][2]

                    if checksum != out: violations.append("{coll_name}/{data_name} violates the checksum policy {out} vs {checksum}".format(**locals()))

                # -- end -- for resources

        # -- end -- for objects

    # -- end -- for collections

    rule_args [2] = join_text_lines( violations )

