import subprocess as sps
import sys, os


def sbatch(job_name="run_py_job", output="run_py_submit.csv", partition="GRID-ALL", array='1-3', wrap="sbatch.py"):

    # sub=['sbatch',
    #     '--job-name={}'.format(job_name),
    #     '--output={}'.format(output),
    #     '--partition={}'.format(partition),
    #     '--array={}'.format(array),
    #     '--ntasks=1',
    #     'START_INDEX=$(( ($SLURM_ARRAY_TASK_ID - 1) * 5 + 1 ))',
    #     'END_INDEX=$(($START_INDEX + 4))',
    #     'Rscript run_bfast_from_shape.R $START_INDEX $END_INDEX',
    #     'wait']

    sub=['sinfo', '-l']

    sub.append('--wrap="{}"'.format(wrap.strip()))
    # print(" ".join(sub))
    process = sps.Popen(" ".join(sub), shell=True, stdout=sps.PIPE)
    stdout = process.communicate()[0].decode("utf-8")
    return(stdout)

def run_cmd(cmd):
    # simplified subprocess.run() of running linux command in python
    # cmd pass in as a list of strings, i.e. cd .. should be ['cd', '..']
    # return screen print as a string
    process=sps.run(cmd, stdout=sps.PIPE)
    print(process.stdout.decode("utf-8"))


# def limit_jobs(limit=20000):
#     l_jobs=run_cmd(['squeue', '-u', '$USER']).split("\n")
#     # limit the total number of jobs in slurm job queue
#     while int(l_jobs) >= limit:
#         time.sleep(300)


# if __name__ == '__main__':
#     sbatch(wrap="python hello.py")



# def sbatch(job_name="py_job", mem='4', dep="", time='3-0', log="submit.out", wrap="python hello.py", add_option=""):