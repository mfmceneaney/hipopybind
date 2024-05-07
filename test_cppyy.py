import cppyy
import sys
import os.path as osp
from glob import glob

# Bind hipo
hipopath = '/group/clas12/packages/hipo/4.0.1/' #NOTE: COULD SET THIS FROM SUBMODULE... OR FROM HIPO ENVIRONMENT VARIABLE
if 'HIPO_CPPYY_HOME' in os.environ.keys():
    hipopath = os.environ['HIPO']
include_path = osp.join(hipopath,'include')
library_path = osp.join(hipopath,'lib')
cppyy.add_include_path(include_path)
cppyy.add_library_path(library_path)
cppyy.load_library('hipo4')
headers = glob(osp.join(hipopath,'include/hipo4/*.h'))
print("DEBUGGING: headers = ",headers)
allowed_basenames = ['reader.h','writer.h','event.h','dictionary.h','bank.h']
for  header in headers:
    if not osp.basename(header) in allowed_basenames: continue
    cppyy.include(header.replace(include_path+osp.sep,'')) #NOTE: Just need to ensure hipopath ends in

# Now hipo classes should be available from cppyy.gbl
from cppyy.gbl import hipo
# from here the syntax is analogous to the C++ example

if len(sys.argv)<=1:
    print('Usage: ',osp.basename(__file__),': <optional: inFile> <optional: numEvents>')
    sys.exit(1)
inFile    = sys.argv[1]      if len(sys.argv)>1 else 'data.hipo'
numEvents = int(sys.argv[2]) if len(sys.argv)>2 else 3

reader = hipo.reader(inFile)
banks  = reader.getBanks([
    "RUN::config",
    "REC::Particle",
    "REC::Calorimeter",
    "REC::Track",
    "REC::Scintillator"])

print("DEBUGGING: type(banks) = ",type(banks))
