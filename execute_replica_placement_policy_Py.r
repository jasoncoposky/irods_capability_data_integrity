execute_replica_placement_policy {
    from irods_capability_integrity_utils import (split_text_lines, )
    violations = ""

    callback.verify_replica_placement(violations)

    for v in split_text_lines(violations):
        callback.writeLine("stdout", v)

INPUT null
OUTPUT ruleExecOut
