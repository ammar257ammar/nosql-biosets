# Project aim and summary 

We want to develop scripts for NoSQL indexing and querying of sample
bioinformatics datasets. 
In the early stages of the project only indexing with Elasticsearch was supported.
Later, we have implemented MongoDB support for all the datasets already included
in the project.
For few datasets (IntEnz, PubTator, HGNC) Neo4j and PostgresSQL support
was added as the 3rd database option. We want to extend Neo4j and PostgresSQL
support to more datasets.

## Datasets supported

* UniProtKB [datasets](
ftp://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/knowledgebase/complete/
) in XML format:
  [`./nosqlbiosets/uniprot`](nosqlbiosets/uniprot)

* IntEnz [dataset](
ftp://ftp.ebi.ac.uk/pub/databases/intenz/xml/
) in XML format, from EMBL-EBI:
  [`./nosqlbiosets/intenz`](nosqlbiosets/intenz)

* MetaNetX [compounds, reactions, and compartments data](
http://www.metanetx.org/mnxdoc/mnxref.html
): [`./nosqlbiosets/metanetx`](./nosqlbiosets/metanetx)

* HMDB [proteins, metabolites datasets](http://www.hmdb.ca/downloads):
  [`./hmdb`](hmdb/)

* HGNC, [genenames.org](http://www.genenames.org/cgi-bin/statistics),
 [data files in json format](
 http://ftp.ebi.ac.uk/pub/databases/genenames/new/json/),
  from EMBL-EBI: [`./geneinfo/index-hgnc-geneinfo.py`](geneinfo/index-hgnc-geneinfo)
  (_not matured yet, tests made with [complete HGNC dataset](
  ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/json/hgnc_complete_set.json)
  and with [protein-coding genes dataset](
  ftp://ftp.ebi.ac.uk/pub/databases/genenames/new/json/locus_groups/protein-coding_gene.json)_) 

* Metabolic network files in [SBML](http://sbml.org) format or
 [PSAMM project's yaml](https://github.com/zhanglab/psamm-model-collection)
  format: [`./nosqlbiosets/pathways/index_metabolic_networks.py`](
  nosqlbiosets/pathways/index_metabolic_networks.py)
   (_recent work, tests made with [BiGG](http://bigg.ucsd.edu/)
    and PSAMM collections_)
  
* PubChem [BioAssay](http://ftp.ncbi.nlm.nih.gov/pubchem/Bioassay) json files:
  [`./nosqlbiosets/pubchem`](
  nosqlbiosets/pubchem)  

* WikiPathways [gpml files](
http://www.wikipathways.org/index.php/Download_Pathways):
  [`./nosqlbiosets/pathways/index_wikipathways.py`](
  ./nosqlbiosets/pathways/index_wikipathways.py)

* PMC [articles](http://ftp.ebi.ac.uk/pub/databases/pmc/manuscripts):
  [`./nosqlbiosets/pubmed/index_pmc_articles.py`](
  ./nosqlbiosets/pubmed/index_pmc_articles.py)

* Ensembl regulatory build [GFF files](
http://ftp.ensembl.org/pub/current_regulation/homo_sapiens):
  [`./geneinfo/ensembl_regbuild.py`]([geneinfo/ensembl_regbuild.py)    

* NCBI PubTator [gene2pub and disease2pub mappings](
http://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator):
  [`./nosqlbiosets/pubtator`](nosqlbiosets/pubtator)

* RNAcentral [identifier mappings](
http://ftp.ebi.ac.uk/pub/databases/RNAcentral/current_release/id_mapping/),
  [`./geneinfo/rnacentral_idmappings.py`](geneinfo/rnacentral_idmappings.py)

* ModelSEED [compounds and reactions data files](
https://github.com/ModelSEED/ModelSEEDDatabase/tree/master/Biochemistry/)
in tsv format:
  [`./nosqlbiosets/kbase/index_modelseed.py`](nosqlbiosets/kbase/index_modelseed.py)

* KEGG [pathway kgml/xml files](
http://www.kegg.jp/kegg/download/Readme/README.kgml):
  [`./nosqlbiosets/kegg/index.py`](nosqlbiosets/kegg/index.py)
  (_KEGG data distribution policy lets us think twice when spending
   time on KEGG data_)
  

We want to connect above datasets as much as possible
and aim to implement scripts with example queries for individual indexes
as well as connected data. We want to implement automated tests as early as
possible, this should help us to understand where we are in minimal time. 

In a separate [project](https://github.com/uludag/hspsdb-indexer)
we have developed index scripts for sequence
similarity search results, either in NCBI-BLAST xml/json formats
or in SAM/BAM formats

## Installation

Download nosqlbiosets project source code and install required libraries:
```bash
$ git clone https://bitbucket.org/hspsdb/nosql-biosets.git
$ cd nosql-biosets
$ pip install -r requirements.txt --user
```

Since we are yet in early stages you may need to check (and modify)
source code of the scripts time to time, for this reason _light install_
nosqlbiosets project to your local Python library/package folders
using the `setup.py` `develop` and `--user` options
that should allow you to run the index scripts from project
source folders:
```bash
$ python setup.py develop --user
```

Default values of the hostname and port numbers of Elasticsearch and MongoDB servers
are read from [`./conf/dbservers.json`](conf/dbservers.json) file.
Save your settings in this file to avoid entering `--host` and `--port`
parameters in command line.

## Usage

Example command lines for downloading UniProt Knowledgebase Swiss-Prot data set
(~680M) and for indexing:
```bash
$ wget ftp://ftp.ebi.ac.uk/pub/databases/uniprot/current_release/\
knowledgebase/complete/uniprot_sprot.xml.gz
```
Make sure your Elasticsearch server is running in your localhost.
If you are new to Elasticsearch and  you are using Linux
the easiest way is to [download Elasticsearch](
https://www.elastic.co/downloads/elasticsearch) with the TAR option (~32M).
After extracting the tar file just `cd` to your Elasticsearch folder
and run `./bin/elasticsearch` command.

Now we can index downloaded UniProt xml file by running the following command
from nosqlbiosets project root folder (typically takes 5 to 8 hours,
we can go to the next step without waiting the termination of whole
indexing process).

```bash
$ ./nosqlbiosets/uniprot/index.py --infile ./uniprot_sprot.xml.gz\
 --host localhost --db Elasticsearch --index uniprot
```
Query top mentioned gene names: 
```bash
curl -XGET "http://localhost:9200/uniprot/_search?pretty=true"\
 -H 'Content-Type: application/json' -d'
{
  "size": 0,
  "aggs": {
    "genes": {
      "terms": {
        "field": "gene.name.#text.keyword",
        "size": 5
      },
      "aggs": {
        "tids": {
          "terms": {
            "field": "gene.name.type.keyword",
            "size": 5
          }
        }
      }
    }
  }
}'
```
Check [`./tests/test_uniprot_queries.py`](tests/test_uniprot_queries.py) 
and [`./nosqlbiosets/uniprot/query.py`](./nosqlbiosets/uniprot/query.py) for
example queries with Elasticsearch and MongoDB.

## Copyright
This project has been developed
at King Abdullah University of Science and Technology, http://www.kaust.edu.sa

## Acknowledgement
Computers and file systems used in developing this work has been maintained by John Hanks
