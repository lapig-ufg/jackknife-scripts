import subprocess
import sys, os

result = subprocess.run(['sinfo', '-l'], stdout=subprocess.PIPE)
print(result.stdout)



#def sbatch(job_name="run_py_job", output="run_py_submit.csv", partition="GRID-ALL", array='1-3'):
    
# submit = subprocess.run(['sinfo', '-l'], stdout=subprocess.PIPE)
# print(submit.stdout)

        # '--job-name={}'.format(job_name),
        # '--output={}'.format(output),
        # '--partition={}'.format(partition),
        # '--array={}'.format(array),
        # '--ntasks=1',
        # 'Rscript run_bfast_from_shape.R 1 3',
        # 'wait']

    #subprocess.run(submit, shell=TRUE, check=TRUE)

    # process = subprocess.Popen(" ".join(sub), shell=True, stdout=subprocess.PIPE)
    # stdout = process.communicate()[0].decode("utf-8")
    # return(stdout)

# def run_cmd(cmd):
#     # simplified subprocess.run() of running linux command in python
#     # cmd pass in as a list of strings, i.e. cd .. should be ['cd', '..']
#     # return screen print as a string
#     process=subprocess.run(cmd, stdout=subprocess.PIPE)
#     print(process.stdout.decode("utf-8"))


# def limit_jobs(limit=20000):
#     l_jobs=run_cmd(['squeue', '-u', '$USER']).split("\n")
#     # limit the total number of jobs in slurm job queue
#     while int(l_jobs) >= limit:
#         time.sleep(300)


# if __name__ == '__main__':
#     sbatch(wrap="python hello.py")



# def sbatch(job_name="py_job", mem='4', dep="", time='3-0', log="submit.out", wrap="python hello.py", add_option=""):

# sbatch -N4 << EOF
# #!/bin/sh
# srun hostname | sort
# EOF