# Single point of truth for an error value
get_error_value(*err) { *err = "ERROR_VALUE" }

# The code to return for the rule engine plugin framework to look for additional PEPs to fire.
RULE_ENGINE_CONTINUE { 5000000 }

# Error code if input is incorrect
SYS_INVALID_INPUT_PARAM { -130000 }

# metadata attribute driving policy for user status
verify_checksum_attribute { "irods::verification::checksum" }

verify_replica_checksum(*all_flag, *resource_name, *violations)
{
    *attr = verify_checksum_attribute

    # get a list of all matching collections given the metadata attribute
    foreach(*row0 in SELECT COLL_NAME, META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = "*attr") {

        *coll_name = *row0.COLL_NAME

        # get a list of all data objects in the given collection
        foreach(*row1 in SELECT COLL_NAME, DATA_NAME WHERE COLL_NAME like "*coll_name%") {

            *coll_name = *row1.COLL_NAME

            *data_name = *row1.DATA_NAME

            if(true == *all_flag) {
                foreach(*row2 in SELECT DATA_REPL_NUM, DATA_CHECKSUM WHERE COLL_NAME = "*coll_name" AND DATA_NAME = "*data_name") {

                    *repl_num = *row2.DATA_REPL_NUM

                    *checksum = *row2.DATA_CHECKSUM

                    msiDataObjChksum("*coll_name/*data_name", "forceChksum=++++replNum=*repl_num", *out)

                    if(*checksum != *out) {
                        *violations = cons("*coll_name/*data_name violates the checksum policy *out vs *checksum", *violations)
                    }

                } # for resources
            }
            else {
                foreach(*row2 in SELECT DATA_REPL_NUM, DATA_CHECKSUM WHERE COLL_NAME = "*coll_name" AND DATA_NAME = "*data_name" AND RESC_NAME = "*resource_name") {

                    *repl_num = *row2.DATA_REPL_NUM

                    msiDataObjChksum("*coll_name/*data_name", "forceChksum=++++replNum=*repl_num", *out)

                    *checksum = *row2.DATA_CHECKSUM

                    if(*checksum != *out) {
                        *violations = cons("*coll_name/*data_name violates the checksum policy *out vs *checksum", *violations)
                    }

                } # for resources
            }

        } # for objects

    } # for collections

} # verify_replica_checksum
