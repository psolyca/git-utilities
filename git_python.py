#!/usr/bin/python

import os, sys, subprocess

def cur_branch():
   # get the current branch
   proc = subprocess.Popen(['git', 'symbolic-ref', '-q', 'HEAD'],
                           stdout=subprocess.PIPE)
   proc.wait()
   current_branch = proc.stdout.read().split('/')[2].strip()
   
   return current_branch


def is_dirty():
   proc = subprocess.Popen(['git', 'diff', '--shortstat'], 
                           stdout=subprocess.PIPE)
   if proc.stdout.read().strip() != "":
      return True
   else:
      return False

def checkout(branch):
   if branch==cur_branch():
      return
   proc = subprocess.check_call(['git', 'checkout', branch]) 

def merge_base( branches ):
   '''returns the most recent common ancestor between branches'''
   result= subprocess.check_output(['git', 'merge-base']+branches)
   assert len(result.splitlines()[0])==40 #SHA1 hash size plus newline
   return result.splitlines()[0]

def merge_base_from_commits_list( l1, l2 ):
   '''returns the most recent common ancestor between lists of commits.
   List MUST BE ORDERED FROM OLD TO RECENT'''
   assert l1[0]==l2[0]
   last= l1[0]
   i=0
   for c1,c2 in zip(l1,l2):
      if c1!=c2:
         return i-1, last #index and hash
      last= c1
      i+=1
   return i-1, last

def commit_author_date( commit ):
   return subprocess.check_output(["git", "log", "-1", '--format=%ad', commit] )
   
def commits_between( old_branch, new_branch, rev= False ):
   '''returns the hashes of the commits between two branches,
   ordered from new to old (unless rev)'''
   result = subprocess.check_output(['git', 'log', '--format=%H', old_branch+"^.."+new_branch]) 
   result= result.splitlines()
   assert all([len(x)==40 for x in result]) #SHA1 hash size
   if rev:
      result= list(reversed(result))
   return result
 
def rebase(base, branch, onto=None, flags=[]):
   args = ['git', 'rebase']
   if onto:
      args+= ['--onto', onto]
   args += flags
   args.append(base)
   args.append(branch)

   proc = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE) 
   rc = proc.wait()
   if rc != 0:
      print proc.stdout.read()
      print "git rebase: execute 'git rebase --continue|--abort', then exit shell to continue the git rebase process"
      subprocess.call(['$SHELL'], shell=True)
   return 0

def create_branch(branchname):
   subprocess.check_call(['git', 'branch', branchname])

def delete_branch(branchname, force=False):
   delete_flag= "-D" if force else "-d"
   subprocess.check_call(['git', 'branch', delete_flag, branchname])

def rename_branch(branch, newbranch):
   subprocess.check_call(['git', 'branch', "-m", branch, newbranch])
 

