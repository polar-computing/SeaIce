from radical.ensemblemd import Kernel
from radical.ensemblemd import PoE
from radical.ensemblemd import EnsemblemdError
from radical.ensemblemd import ResourceHandle

from radical.ensemblemd.engine import get_engine
from qbird import kernel_qbird
get_engine().add_kernel_plugin(kernel_qbird)

import os
import json
import sys

# ------------------------------------------------------------------------------
# Set default verbosity

if os.environ.get('RADICAL_ENTK_VERBOSE') == None:
	os.environ['RADICAL_ENTK_VERBOSE'] = 'REPORT'


class MyApp(PoE):

	def __init__(self, stages,instances):
		 PoE.__init__(self, stages,instances)

	def stage_1(self, instance):
		k = Kernel(name="qbird")
		k.upload_input_data = ['SeaIceUnSuperGMM.py']
		k.arguments = ["--script=SeaIceUnSuperGMM.py",
				"--imagepath=/home/vivek91/xsede-hack/IMG/XinImages/TEST/072610_00332.jpg",
				"--trainingpath=/home/vivek91/xsede-hack/IMG/XinImages/TRAINING/",
				"--num_train=3",
				"--icetypes=4"]
		k.download_output_data = ["labelledImage3trainingImages.png > image_{0}.png".format(instance)]
		return k

if __name__ == "__main__":

	# use the resource specified as argument, fall back to localhost
	if   len(sys.argv)  > 2: 
		print 'Usage:\t%s [resource]\n\n' % sys.argv[0]
		sys.exit(1)
	elif len(sys.argv) == 2: 
		resource = sys.argv[1]
	else: 
		resource = 'local.localhost'

	try:

		with open('%s/config.json'%os.path.dirname(os.path.abspath(__file__))) as data_file:    
			config = json.load(data_file)


		# Create a new resource handle with one resource and a fixed
		# number of cores and runtime.
		cluster = ResourceHandle(
				resource=resource,
				cores=config[resource]["cores"],
				walltime=60,
				username='vivek91',

				project=config[resource]['project'],
				access_schema = config[resource]['schema'],
				queue = config[resource]['queue'],
				database_url='mongodb://rp:rp@ds015335.mlab.com:15335/rp',
			)

		# Allocate the resources.
		cluster.allocate()

		# Set the 'instances' of the BagofTasks to 16. This means that 16 instances
		# of each BagofTasks step are executed.
		app = MyApp(stages=1,instances=1)

		cluster.run(app)

	except EnsemblemdError, er:

		print "Ensemble MD Toolkit Error: {0}".format(str(er))
		raise # Just raise the execption again to get the backtrace

	try:
		# Deallocate the resources. 
		cluster.deallocate()

	except:
		pass
