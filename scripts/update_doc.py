"""script to update documentation."""
import argparse  # type: ignore
import os  # type: ignore

# Print Banner
print("----------------------------------------------------------------")
print("Updating Documentation, point github sites to the correct branch")
print("----------------------------------------------------------------")

# Get the branch argument
parser = argparse.ArgumentParser()
parser.add_argument("branch", help="The doucmentation branch")
args = parser.parse_args()

doc_branch = args.branch

# Run a command and get the output as a string

current_branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
print("Current Branch: " + current_branch)
print("Documentation Branch: " + doc_branch)

os.system("git checkout " + doc_branch + " > /dev/null")
print("Current Branch: " + doc_branch)

os.system("git add * > /dev/null")
os.system("git commit -m 'Task: Update Documentation' > /dev/null")
os.system("git push --set-upstream origin " + doc_branch)
os.system("git checkout " + current_branch + "  > /dev/null")
