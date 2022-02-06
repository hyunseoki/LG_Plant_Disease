$cmd0 = "python train_cnn.py --device cuda:0 --model 'tf_efficientnetv2_s' --lr 0.0005 --epochs 2 --base_folder 'C:\Users\bed1\src\dacon_farm\data\train' --label_fn 'C:\Users\bed1\src\dacon_farm\data\train.csv'"
$host.UI.RawUI.WindowTitle = $cmd0
Invoke-Expression -Command $cmd0