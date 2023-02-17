import atexit
import sys
import coverage
cov = coverage.coverage()
cov.start()

from .main import app
def save_coverage():
	print(sys.stderr, "saving coverage")
	# save coverage report to xml file
	cov.xml_report(outfile="coverage.xml")
	cov.stop()
	cov.save()

atexit.register(save_coverage)
print("finish testing coverage!")
