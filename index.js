const express = require('express');
const multer = require('multer');
const ffmpeg = require('fluent-ffmpeg');
const path = require('path');
const fs = require('fs');

const app = express();
const port = process.env.PORT || 3000;

const upload = multer({ dest: 'uploads/' });

app.get('/', (req, res) => {
    res.send('Video overlay service is running.');
});

app.post('/overlay', upload.fields([{ name: 'video1' }, { name: 'video2' }]), (req, res) => {
    console.log('Received a POST request to /overlay');
    console.log('Files:', req.files);

    if (!req.files || !req.files.video1 || !req.files.video2) {
        console.error('Missing files in request');
        return res.status(400).send('Both video1 and video2 files are required');
    }

    const video1Path = req.files.video1[0].path;
    const video2Path = req.files.video2[0].path;
    const outputPath = path.join('output', 'output.mp4');

    ffmpeg()
        .input(video1Path)
        .input(video2Path)
        .complexFilter('[0:v][1:v] overlay=0:0')
        .save(outputPath)
        .on('end', () => {
            console.log('Video processing completed');
            res.download(outputPath, 'output.mp4', (err) => {
                if (err) {
                    console.error(`Error sending file: ${err.message}`);
                }

                // Clean up uploaded and output files
                fs.unlink(video1Path, () => {});
                fs.unlink(video2Path, () => {});
                fs.unlink(outputPath, () => {});
            });
        })
        .on('error', (err) => {
            console.error(`Error: ${err.message}`);
            res.status(500).send('An error occurred during video processing');
        });
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
