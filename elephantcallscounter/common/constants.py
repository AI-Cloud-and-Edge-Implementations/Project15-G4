import os
from elephantcallscounter.utils.path_utils import get_project_root

TRAINING_FILE_PATH_DEFAULT = os.path.join(
                get_project_root(), 'data/metadata/nn_ele_hb_00-24hr_TrainingSet_v2.txt'
            )
TEST_PATH_DEFAULT = os.path.join(
                get_project_root(), 'data/metadata/nn_ele_00-24hr_GeneralTest_v4.txt'
            )