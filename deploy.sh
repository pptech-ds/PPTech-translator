sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install gcc -y
sudo apt-get install g++ -y
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
bash ~/miniconda.sh -b -p $HOME/miniconda
eval "$(/home/ubuntu/miniconda/bin/conda shell.bash hook)"
conda init
conda create -n translator python=3.6.8 -y
conda activate translator
pip install -r requirements.txt
git clone https://github.com/pytorch/fairseq
cd fairseq
pip install --editable .
cd ..
python main.py