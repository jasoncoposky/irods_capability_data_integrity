def main(rule_args, callback, rei):
    from irods_capability_integrity_utils import (TRUE, split_text_lines)

    violations = ""
    callback.verify_replica_checksum (TRUE(), "", violations)
    violations = retval ['arguments'][2]

    for v in split_text_lines( violations ):
        callback.writeLine( "stdout", v )

INPUT null
OUTPUT ruleExecOut
