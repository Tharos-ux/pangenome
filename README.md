# Genouest

**Prérequis** :

+ Trouver son path : eval echo "~$USER"
+ Permissions clé RSA : chmod 400 ~/.ssh/id_rsa_genouest
+ Ajout clé générée par site Genouest : ssh-add $HOME/.ssh/id_rsa_genouest
+ Connexion : ssh sdubois@genossh.genouest.org

**Copie de fichiers depuis Genouest vers session**

```bash
scp sdubois@genossh.genouest.org:/scratch/sdubois/Stage_M2/pangenome/data/ /udd/sidubois/Documents/Code/

scp -r sdubois@genossh.genouest.org:/home/genouest/genscale/sdubois/wisp/output/small /udd/sidubois/Stage/output
```
**Copie de fichiers depuis session vers Genouest**

```bash
scp file.txt sdubois@genossh.genouest.org:/groups/thermin/StreptoThermoGenomes

scp file.txt sdubois@genossh.genouest.org:/home/genouest/genscale/sdubois
```

cd /scratch/sdubois/Stage_M2/pangenome/
srun --pty bash
. /local/env/envconda.sh
conda activate .env/