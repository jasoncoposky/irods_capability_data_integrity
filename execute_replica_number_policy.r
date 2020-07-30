execute_replica_number_policy {
    *violations = list()

    verify_replica_number(*violations)

    foreach(*v in *violations) {
        writeLine("stdout", "*v")
    }
}
INPUT null
OUTPUT ruleExecOut
