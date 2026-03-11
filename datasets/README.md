# Datasets for Meeting AI System

This directory contains references and loaders for training datasets.

## Speech Recognition Datasets

### Common Voice (Mozilla)
- **URL**: https://commonvoice.mozilla.org/
- **Size**: 2,500+ hours (English), 100+ hours (Korean)
- **Use**: Fine-tuning Whisper for multilingual ASR
```bash
pip install datasets
python -c "from datasets import load_dataset; ds = load_dataset('mozilla-foundation/common_voice_13_0', 'ko', split='train')"
```

### LibriSpeech
- **URL**: https://www.openslr.org/12
- **Size**: 1,000 hours clean English speech
- **Use**: Baseline ASR training / evaluation
```bash
python -c "from datasets import load_dataset; ds = load_dataset('librispeech_asr', 'clean', split='train.100')"
```

### KsponSpeech (Korean)
- **URL**: https://aihub.or.kr/
- **Size**: 1,000+ hours Korean conversational speech
- **Use**: Korean ASR fine-tuning

---

## Translation Datasets

### OPUS (Open Parallel Universal corpus)
- **URL**: https://opus.nlpl.eu/
- **Korean-English pairs**: 5M+ sentence pairs
- **Use**: Fine-tuning MarianMT
```bash
python -c "from datasets import load_dataset; ds = load_dataset('opus_books', 'en-ko')"
```

### CCAligned
- **URL**: https://www.statmt.org/cc-aligned/
- **Use**: Large-scale parallel corpus for KO-EN

---

## Summarization Datasets

### SAMSum
- **URL**: https://huggingface.co/datasets/samsum
- **Size**: 16K dialogue summaries
- **Use**: Fine-tuning T5 for meeting summarization
```bash
python -c "from datasets import load_dataset; ds = load_dataset('samsum')"
```

### DialogSum
- **URL**: https://huggingface.co/datasets/knkarthick/dialogsum
- **Size**: 13K dialogue summaries
- **Use**: Additional training data for summarization

---

## Speaker Diarization Datasets

### VoxCeleb
- **URL**: https://www.robots.ox.ac.uk/~vgg/data/voxceleb/
- **Size**: 7,000+ speakers
- **Use**: Speaker verification and diarization

### AMI Corpus
- **URL**: https://groups.inf.ed.ac.uk/ami/corpus/
- **Size**: 100 hours of meeting recordings
- **Use**: Meeting-specific diarization training

---

## Data Storage

Downloaded datasets should be placed in `datasets/data/` (gitignored).

```
datasets/
├── data/
│   ├── common_voice/
│   ├── librispeech/
│   ├── opus_ko_en/
│   └── samsum/
└── README.md
```
