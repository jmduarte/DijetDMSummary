what = {
	"UA2.csv":"gq",
	"CDF_Run1.csv":"gq",
	"CDF_Run2.csv":"gq",
	"gBMZB_ATLAS_all_fbinv.csv":"gB",
	"CMS_Scouting.csv":"gB",
}
for filename in ["UA2.csv", "CDF_Run1.csv", "CDF_Run2.csv", "gBMZB_ATLAS_all_fbinv.csv", "CMS_Scouting.csv"]:
	with open(filename, 'r') as f:
		new_file = open("../{}.dat".format(filename.split(".")[0]), 'w')
		new_file.write("# m_med gq\n")
		for line in f:
			line_contents = line.split(",")
			m = float(line_contents[0])
			if what[filename] == "gB":
				gB = float(line_contents[1])
				gq = gB / 6
			else:
				gq = float(line_contents[1])
			new_file.write("{} {}\n".format(m, gq))
		new_file.close()

