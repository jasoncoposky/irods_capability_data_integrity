__all__ = ['verify_replica_checksum']
from genquery import Query, AS_DICT
from irods_capability_integrity_utils import *


def checksum_test(callback, object_path, repl_num):
    try:
        rv = callback.msiDataObjChksum( object_path,
                                        "verifyChksum=++++replNum={}".format(repl_num), "" )
    except RuntimeError as exc :
        return ('MISMATCH' if "status [USER_CHKSUM_MISMATCH]" in str(exc)
                else 'OTHER_ERROR')

    return rv['arguments'][2]


def verify_replica_checksum (rule_args, callback, rei):

    (all_flag,  resource_name,  violations) = rule_args

    violations = split_text_lines( violations )

    attr = verify_checksum_attribute()

    for row0 in Query (callback, ['COLL_NAME','META_COLL_ATTR_VALUE'],
                       "META_COLL_ATTR_NAME = '{}'".format(attr), AS_DICT):

        coll_name = row0 ['COLL_NAME']

        for row1 in Query (callback, ['COLL_NAME','DATA_NAME'], 
                           "COLL_NAME like '{}%'".format( coll_name ), AS_DICT):
            coll_name = row1['COLL_NAME']
            data_name = row1['DATA_NAME']

            condition = "COLL_NAME = '{0}' AND DATA_NAME = '{1}'" .format( coll_name, data_name)

            if TRUE() != all_flag:
                condition += " and RESC_NAME = '{0}'".format(resource_name)

            for row2 in Query (callback, ['DATA_REPL_NUM', 'DATA_CHECKSUM'], condition, AS_DICT ):

                checksum = row2['DATA_CHECKSUM']
                repl_num = row2['DATA_REPL_NUM']

                out = checksum_test (callback, "{}/{}".format(coll_name,data_name), repl_num)

                if checksum != out and out == 'MISMATCH':
                    violations.append("{coll_name}/{data_name} violates the checksum policy {out} vs {checksum}".format(**locals()))

            # -- end -- for resources

        # -- end -- for objects

    # -- end -- for collections

    rule_args [2] = join_text_lines( violations )

