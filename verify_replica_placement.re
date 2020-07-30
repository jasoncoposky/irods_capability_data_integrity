# Single point of truth for an error value
get_error_value(*err) { *err = "ERROR_VALUE" }

# The code to return for the rule engine plugin framework to look for additional PEPs to fire.
RULE_ENGINE_CONTINUE { 5000000 }

# Error code if input is incorrect
SYS_INVALID_INPUT_PARAM { -130000 }

# metadata attribute driving policy for user status
verify_replicas_attribute { "irods::verification::replica_placement" }

verify_replica_placement(*violations)
{
    *attr = verify_replicas_attribute

    # get a list of all matching collections given the metadata attribute
    foreach(*row0 in SELECT COLL_NAME, META_COLL_ATTR_VALUE WHERE META_COLL_ATTR_NAME = "*attr") {
        *resource_list = *row0.META_COLL_ATTR_VALUE

        *number_of_resources = size(split(*resource_list, ","))

        *coll_name = *row0.COLL_NAME

        # get a list of all data objects in the given collection
        foreach(*row1 in SELECT COLL_NAME, DATA_NAME WHERE COLL_NAME like "*coll_name%") {

            *matched = 0

            *coll_name = *row1.COLL_NAME
            *data_name = *row1.DATA_NAME

            # get all of the resource names where this objects replicas reside
            foreach(*row2 in SELECT RESC_NAME WHERE COLL_NAME = "*coll_name" AND DATA_NAME = "*data_name") {
                *resource_name = *row2.RESC_NAME

                 # set modify for all collaborators
                 *split_list = split(*resource_list, ",")

                 while(size(*split_list) > 0) {
                     # pull head of list
                     *name = str(hd(*split_list))

                     # subset remainder of list
                     *split_list = tl(*split_list)

                     # chomp space
                     *name = triml(*name, ' ')
                     *name = trimr(*name, ' ')

                     # set write permission for collaborator
                     if(*name == *resource_name) {
                         *matched = *matched + 1
                     }
                 }

            } # for resources

            if(*matched < *number_of_resources) {
                *violations = cons("*coll_name/*data_name violates the placement policy " ++ *resource_list, *violations)
            }

        } # for objects

    } # for collections

} # verify_replica_placement
