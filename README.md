# 🎬 Caption This! - AI-Powered Video Transcription & Translation

An automated desktop application that generates accurate SRT subtitle files from videos using OpenAI's Whisper model. Transcribe and translate video content with ease through both CLI and GUI interfaces.

## 🎯 Overview

**Caption This!** is a Python-based tool that leverages OpenAI's Whisper AI model to automatically transcribe video audio into subtitle files. Whether you need transcriptions in the original language or English translations, Caption This! handles the heavy lifting of audio extraction, transcription, and SRT file generation.

Perfect for content creators, translators, accessibility professionals, and anyone needing reliable video captions.

## ✨ Key Features

- **AI-Powered Transcription** - Uses OpenAI's Whisper model for high-accuracy speech recognition
- **Dual Interface** - Choose between command-line or graphical user interface
- **Multi-Language Support** - Transcribe in original language or translate to English
- **Automated Audio Extraction** - Automatically extracts audio from video files using FFmpeg
- **SRT File Generation** - Outputs industry-standard subtitle files with precise timestamps
- **Batch Processing** - Process multiple transcription tasks sequentially
- **Windows Optimized** - Includes batch files and VBS launcher for easy Windows execution

## 🛠️ Tech Stack

- **Python 3.x** - Core programming language
- **OpenAI Whisper** - State-of-the-art speech recognition model
- **FFmpeg** - Audio extraction and processing
- **Tkinter** - GUI framework for desktop interface
- **PyFiglet** - ASCII art for CLI branding

## 🚀 Getting Started

### Prerequisites

Ensure you have the following installed:
- Python 3.7 or higher
- FFmpeg (must be in system PATH)

### Installation

```bash
# Clone the repository
git clone https://github.com/ETVO/caption-this.git
cd caption-this

# Install Python dependencies
pip install -r requirements.txt
```

### Usage

#### GUI Mode (Recommended for Windows)

**Windows:**
```bash
# Double-click Caption-This!.vbs in the dist folder
# Or run:
dist\run_gui.bat
```

**Mac/Linux:**
```bash
python gui.py
```

#### CLI Mode

**Windows:**
```bash
dist\run_main.bat
```

**Mac/Linux:**
```bash
python main.py
```

### Workflow

1. **Select Video** - Choose the video file you want to transcribe
2. **Choose Task**:
   - **Transcribe** - Generate subtitles in original language
   - **Translate** - Translate audio to English
   - **Both** - Create both original and translated versions
3. **Set Output Directory** - Choose where to save SRT files (default: `caption-this/`)
4. **Process** - The app extracts audio, transcribes it, and generates SRT files
5. **Save** - SRT files are saved with `_Original.srt` or `_Translated.srt` suffixes

## 📁 Project Structure

```
caption-this/
├── main.py              # CLI interface
├── gui.py               # GUI interface
├── transcription.py     # Whisper model integration
├── utils.py             # Helper functions
├── requirements.txt     # Python dependencies
├── icon.ico            # Application icon
└── dist/               # Windows launchers
    ├── Caption-This!.vbs
    ├── run_gui.bat
    └── run_main.bat
```

## 💡 Use Cases

- **Content Creators** - Add subtitles to YouTube, TikTok, and social media videos
- **Translators** - Generate English translations of foreign language content
- **Accessibility** - Make video content accessible to deaf and hard-of-hearing audiences
- **Education** - Create transcripts for lectures and educational videos
- **Documentation** - Transcribe interviews, meetings, and presentations

## 🔧 Technical Details

### Supported Video Formats
Any format supported by FFmpeg (MP4, AVI, MOV, MKV, WebM, etc.)

### Whisper Model
Caption This! uses OpenAI's Whisper model, which supports:
- 99 languages for transcription
- English translation from any source language
- High accuracy even with background noise or accents

### Output Format
Standard SRT (SubRip) format with:
- Sequential numbering
- Timecode stamps (HH:MM:SS,mmm --> HH:MM:SS,mmm)
- UTF-8 encoding for international characters

## 🚀 Possible Future Enhancements

- Detect if audio is already in English when "Both" is selected and skip duplicate processing
- Add support for additional subtitle formats (VTT, ASS)
- Implement batch video processing
- Add model size selection (tiny, base, small, medium, large)
- GPU acceleration support

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

## 📄 License

This project is open source and available for personal and commercial use.

## 👤 Author

**Estevão Pereira Rolim** - [@ETVO](https://github.com/ETVO) | [LinkedIn](https://linkedin.com/in/estevao-p-rolim)

---

*Built with Python and OpenAI Whisper for automated video transcription and translation.*

*README generated in collaboration with Claude AI.*
