import fastbook
from fastbook import *
from fastai.vision.widgets import *

from elephantcallscounter.utils.path_utils import get_project_root
from elephantcallscounter.utils.path_utils import join_paths


def fastapi_run():
    fastbook.setup_book()

    path = Path(join_paths(get_project_root(), "data/spectrograms_boxed/"))

    fns = fastbook.get_image_files(path)

    elephants = DataBlock(
        blocks = (ImageBlock, CategoryBlock),
        get_items = get_image_files,
        splitter = RandomSplitter(valid_pct = 0.2, seed = 42),
        get_y = parent_label,
        item_tfms = Resize(128))

    dls = elephants.dataloaders(path)

    dls.valid.show_batch(max_n = 4, nrows = 1)

    # Looking at different ways to augment the data - squishing
    elephants = elephants.new(item_tfms = Resize(128, ResizeMethod.Squish))
    dls = elephants.dataloaders(path)
    dls.valid.show_batch(max_n = 4, nrows = 1)

    # Looking at different ways to augment the data - padding
    elephants = elephants.new(item_tfms = Resize(128, ResizeMethod.Pad, pad_mode = 'zeros'))
    dls = elephants.dataloaders(path)
    dls.valid.show_batch(max_n = 4, nrows = 1)

    # Looking at different ways to augment the data - cropping
    elephants = elephants.new(item_tfms = RandomResizedCrop(128, min_scale = 0.3))
    dls = elephants.dataloaders(path)
    dls.train.show_batch(max_n = 4, nrows = 1, unique = True)

    # Looking at different ways to augment the data - augmenting and making more
    # elephants = elephants.new(item_tfms=Resize(128), batch_tfms=aug_transforms(mult=2))
    # dls = elephants.dataloaders(path)
    # dls.train.show_batch(max_n=8, nrows=2, unique=True)


    elephants = elephants.new(
        item_tfms = RandomResizedCrop(224, min_scale = 0.5),
        batch_tfms = aug_transforms())
    dls = elephants.dataloaders(path)

    learn = cnn_learner(dls, resnet18, metrics = error_rate)
    learn.fine_tune(4)

    interp = ClassificationInterpretation.from_learner(learn)
    interp.plot_confusion_matrix()

    interp.plot_top_losses(5, nrows = 5)

    learn.export('/content/gdrive/My Drive/5-project15/elephants_export.pkl')

    path = Path('/content/gdrive/My Drive/5-project15')
    path.ls(file_exts = '.pkl')

    learn_inf = load_learner(path / 'elephants_export.pkl')

    learn_inf.predict(join_paths())

    print(learn_inf.dls.vocab)
