#!/usr/bin/env python

"""A kernel that executes the qbird python script
"""

__author__    = "Vivek Balasubramanian"

from copy import deepcopy

from radical.ensemblemd.exceptions import ArgumentError
from radical.ensemblemd.exceptions import NoKernelConfigurationError
from radical.ensemblemd.engine import get_engine
from radical.ensemblemd.kernel_plugins.kernel_base import KernelBase

# ------------------------------------------------------------------------------

_KERNEL_INFO = {

	"name":         "qbird",
	"description":  "Molecular Dynamics with Amber software package http://ambermd.org/",
	"arguments":   {
			"--script=":
						{
							"mandatory": True,
							"description": "Image analysis script to be executed"
						},
			"--imagepath=":	
						{
							"mandatory": True,
							"description": "Path to the classified image"
						},
			"--trainingpath=":
						{
							"mandatory": True,
							"description": "Path to training images"
						},
			"--num_train=":
						{
							"mandatory": True,
							"description": "Number of training images to be used"
						},
			"--icetypes=":
						{
							"mandatory": True,
							"description": "Number of ice types (aka classifiers)"
						}
			},
	"machine_configs": 
	{
		"xsede.comet":
		{
				"environment" : {},
				"pre_exec"    : [	"module load python", 
						"module load gdal"],
				"executable"  : ["python"],
				"uses_mpi"    : False
		},
        
	}
}


# ------------------------------------------------------------------------------
#
class kernel_qbird(KernelBase):

	def __init__(self):

		super(kernel_qbird, self).__init__(_KERNEL_INFO)
		"""Le constructor."""
				
	# --------------------------------------------------------------------------
	#
	@staticmethod
	def get_name():
		return _KERNEL_INFO["name"]
		

	def _bind_to_resource(self, resource_key):
		
		if resource_key not in _KERNEL_INFO["machine_configs"]:
			if "*" in _KERNEL_INFO["machine_configs"]:
				# Fall-back to generic resource key
				resource_key = "*"
			else:
				raise NoKernelConfigurationError(kernel_name=_KERNEL_INFO["name"], resource_key=resource_key)

		cfg = _KERNEL_INFO["machine_configs"][resource_key]

		#change to pmemd.MPI by splitting into two kernels
		arguments = [	'{0}'.format(self.get_arg("--script=")),
				'--imagepath', '{0}'.format(self.get_arg("--imagepath=")),
				'--trainingpath', '{0}'.format(self.get_arg("--trainingpath=")),
				'--num_train', '{0}'.format(self.get_arg("--num_train=")),
				'--icetypes', '{0}'.format(self.get_arg("--icetypes="))
				]
	   
		self._executable  = cfg["executable"]
		self._arguments   = arguments
		self._environment = cfg["environment"]
		self._uses_mpi    = cfg["uses_mpi"]
		self._pre_exec    = cfg["pre_exec"] 

# ------------------------------------------------------------------------------
