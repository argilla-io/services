#/bin/sh

echo "Downloading [en] model..."
python -m spacy.en.download

echo "Model [en] installed"
# while true;
# do
echo "Running server on port 7000"
python app.py
# done
