
def get_error_value           ()   : return "ERROR_VALUE"
def RULE_ENGINE_CONTINUE      ()   : return 5000000
def SYS_INVALID_INPUT_PARAM   ()   : return -130000
def verify_replicas_attribute ()   : return "irods::verification::replica_placement"
def verify_checksum_attribute ()   : return "irods::verification::checksum"
def verify_replica_number_attribute ()   : return "irods::verification::replica_number"

def TRUE(): return "true"

def split_text_lines( string_in ) :
    return filter (None, string_in.split("\n"))

def join_text_lines( list_in ) :
    return "\n".join(filter(None, list_in)) + "\n"

