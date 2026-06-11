# Define permission flags
READ = 4      # binary: 100
WRITE = 2     # binary: 010
EXECUTE = 1   # binary: 001

# User's permission score
user_permission = 6  # binary: 110

# Test if WRITE permission is enabled
if user_permission & WRITE:
    print("WRITE permission enabled")
else:
    print("WRITE permission not enabled")
