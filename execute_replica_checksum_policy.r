execute_replica_checksum_policy {
    *violations = list()

    # all_flag      : checksum all replicas
    # resource_name : if all_flag is false, provide a resource name
    # violations    : list of violating objects
    verify_replica_checksum(true, "", *violations)

    foreach(*v in *violations) {
        writeLine("stdout", "*v")
    }
}
INPUT null
OUTPUT ruleExecOut
