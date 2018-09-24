import subprocess

a=subprocess.check_output("gsutil du -ch  gs://b-ao-product-mock/685372f7-1f01-40e2-bc10-94a4bdd6f300/clips/0:00:00.000_00:05:00/1000_originalclip/0:00:00.000_00:05:00/0:00:00.000_00:05:00/",shell=True)
b=a.split('\n')
print ("b",b[-2])
