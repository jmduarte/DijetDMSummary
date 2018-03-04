import os
import sys
import re
import ROOT
from ROOT import *
from math import sqrt


class DijetData:
	def __init__(self, name):
		self.name = name
		self._data_loaded = False # Data should be loaded only once
		self._sqrt_s = 0 # COM energy needed for conversions

		self._reference_xses = {
			8.:{
				"gq0":0.25, 
				"txt":os.path.expandvars("data/reference/ZPrime_8TeV_gq0p25.dat")
			},
			13.:{}
		}

	def set_sqrts(self, sqrt_s):
		self._sqrt_s = sqrt_s

	# Load input data. Header line is used to determine subsequent processing
	# @param txt: path to text file with input data
	# First line of txt should be # mmed <name>, where <name> = gq or xs#, where #=com energy
	def load_data(self, txt):
		with open(txt, 'r') as f:
			header_contents = f.readline().split()
			if not header_contents[0] == "#":
				print "[dijet_data::load_data] ERROR : Input file {} is missing a header row, so I don't know what the y-axis is.".format(txt)
				sys.exit(1)
			data_name = header_contents[2]
		if data_name == "gq":
			self.load_gq(txt)
		elif "xs" in data_name:
			re_xs = re.compile("xs(?P<sqrts>\d+)")
			re_xs_result = re_xs.search(data_name)
			if not re_xs_result:
				print "[dijet_data::load_data] ERROR : Couldn't parse sqrts out of data_name {}. It should have format xs#, #=sqrts".format(data_name)
				sys.exit(1)
			sqrts = float(re_xs_result.group("sqrts"))
			self.load_xs(txt, sqrts)


	# Load gq values.
	# @ param gq_txt = path to text file with mass \t gq, one per row.
	def load_gq(self, gq_txt):
		self._masses = []
		self._gqs = []
		self._graph = None
		with open(gq_txt, 'r') as f:
			for line in f:
				if line[0] == "#":
					continue
				line_contents = line.split()
				self._masses.append(float(line_contents[0]))
				self._gqs.append(float(line_contents[1]))
		self._data_loaded = True
		self.create_graph()
		#self.print_gq()

	# Load xs values
	# @ param xs _txt = path to text file with mass \t xs, one per row.
	# Note that the xs should be xs*BR(qq), where q=any quark (including top). The reference cross sections assuming a Z' with universal quark coupling.
	# The conversion is g_q = 0.25 * sqrt(xs(95% CLlimit) / xs(gq=0.25))
	# Also note: linear interpolation is used for the reference xses
	def load_xs(self, xs_txt, sqrts=13):
		self._masses = []
		self._gqs = []

		# Extract xses from txt file
		xses = []
		with open(xs_txt, 'r') as f:
			for line in f:
				if line[0] == "#":
					continue
				line_contents = line.split()
				self._masses.append(float(line_contents[0]))
				xses.append(float(line_contents[1]))

		# Load reference xses
		reference_mass_xs = []
		with open(self._reference_xses[sqrts]["txt"], "r") as f:
			for line in f:
				if line[0] == "#":
					continue
				line_contents = line.split()
				reference_mass_xs.append((float(line_contents[0]), float(line_contents[1])))
		reference_mass_xs.sort(key=lambda x: x[0])
		reference_xs_graph = TGraph(len(reference_mass_xs))
		for i, mass_xs in enumerate(reference_mass_xs):
			reference_xs_graph.SetPoint(i, mass_xs[0], mass_xs[1])

		# Do conversions
		for i, mass in enumerate(self._masses):
			print "[debug] Conversion for mass {} = {} * sqrt({} / {}) = {}".format(mass, self._reference_xses[sqrts]["gq0"], xses[i], reference_xs_graph.Eval(mass), self._reference_xses[sqrts]["gq0"] * sqrt(xses[i] / reference_xs_graph.Eval(mass)))
			self._gqs.append(self._reference_xses[sqrts]["gq0"] * sqrt(xses[i] / reference_xs_graph.Eval(mass)))

		self._data_loaded = True
		self.create_graph()
		#self.print_gq()

	def create_graph(self):
		if not self._data_loaded:
			print "[dijet_data::create_graph] ERROR : Call to create_graph before loading data"
			sys.exit(1)
		self._graph = TGraph(len(self._masses))
		for i in xrange(len(self._masses)):
			self._graph.SetPoint(i, self._masses[i], self._gqs[i])

	def print_gq(self):
		print "[dijet_data::print_gq] INFO : Print mass : g_q values for data {}".format(self.name)
		for i in xrange(len(self._masses)):
			print "[dijet_data::print_gq] INFO :\t{} => {}".format(self._masses[i], self._gqs[i])

	def get_gq(self):
		if not self._data_loaded:
			print "[dijet_data::get_gq] ERROR : Call to get_gq before loading data"
			sys.exit(1)
		return self._gqs

	def get_masses(self):
		if not self._data_loaded:
			print "[dijet_data::get_masses] ERROR : Call to get_masses before loading data"
			sys.exit(1)
		return self._masses

	def get_graph(self):
		if not self._data_loaded:
			print "[dijet_data::get_graph] ERROR : Call to get_graph before loading data"
			sys.exit(1)

		return self._graph
