### Start a new repository
# git init / git clone set up

# git start. note: after travel into your directory
git init

## Configure work stations owner of repository
git config --global user.name "Paul Z. Cheng"
git config --global user.email paul.z.cheng@gmail.com
git config --global core.editor atom

## git init set up
cd to/your/favoriate/directory
git init -b <name of your choosing>
# if not specifed init branch will be "master"

# ..... some awesome code session later
git add .
git commit -m "First commit of greatness."

# git remote setup
git remote add origin <Remote URL>

# check remote setup
git remote -v

# push to origin
git push -u origin <name of your choosing>


## Clone a directory
git clone < git URL >
# ..... some awesome code session later and as above

# git remote setup
git remote add origin <Remote URL>

# check remote setup
git remote -v

# push to origin
git push -u origin master


## Branching
# Check out your current listed branches
git branch

# make a branch out of current working area
git branch new_master

#switch branches
git checkout master

# make and switch
git checkout -b master_3

# check the difference between two state
git diff "branch 1" "branch 2"

## some awesome coding and editing of your working area later
# check working area has any need to update
git status

# ADD
git add "file names"  # one file
git add .             # everything that has been changed

# Commit related to "document your add"
git commit -m "xx files update"
# change message
git commit -amend -m "change"

# check out commits
git log

# Alias: simplified commands
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.st status
