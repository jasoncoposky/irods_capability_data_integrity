def main(rule_args, callback, rei):
    from irods_capability_integrity_utils import (split_text_lines, )

    violations = ""
    retval = callback.verify_replica_number(violations)
    violations =  retval['arguments'][0]

    for v in split_text_lines(violations):
        callback.writeLine("stdout", v)

INPUT null
OUTPUT ruleExecOut
