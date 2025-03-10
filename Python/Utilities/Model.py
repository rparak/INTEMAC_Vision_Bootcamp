def Freeze_Backbone(trainer):
  """
  Description:
    Function to freeze the backbone layers of the model.

    Reference:
      https://docs.ultralytics.com/yolov5/tutorials/transfer_learning_with_frozen_layers/

    Note:
      The backbone of the model consists of layers 0-9 (10 layers).
  """

  # Number of layers to be frozen.
  num_frozen_layers = 10

  # Express the model.
  model = trainer.model

  print('[INFO] Freeze the backbone layers of the model:')
  freeze = [f'model.{x}.' for x in range(num_frozen_layers)]
  for k, v in model.named_parameters(): 
      v.requires_grad = True
      if any(x in k for x in freeze):
          print(f'[INFO] Freezing: {k}') 
          v.requires_grad = False