#include "ChartGenerator.h"
#include <aubio/aubio.h>
#include <cmath>
#include <algorithm>
#include <numeric>

bool ChartGenerator::analyze(const std::string& audioPath, AudioFeatures& out) {
    // ── 1. Detect BPM ──
    {
        aubio_source_t* src = new_aubio_source(audioPath.c_str(), 0, 1024);
        if (!src) return false;
        uint_t sr = aubio_source_get_samplerate(src);

        aubio_tempo_t* tempo = new_aubio_tempo("default", 1024, 512, sr);
        fvec_t* buf = new_fvec(1024);
        fvec_t* beatOut = new_fvec(2);

        out.bpm = 140;
        float lastBeat = -1;
        int beatCount = 0;
        std::vector<float> beatTimes;

        uint_t read = 0;
        do {
            aubio_source_do(src, buf, &read);
            aubio_tempo_do(tempo, buf, beatOut);
            if (beatOut->data[0] != 0) {
                float t = aubio_tempo_get_last_s(tempo);
                beatTimes.push_back(t);
                lastBeat = t;
                beatCount++;
            }
        } while (read == 1024);

        // Derive BPM from beat intervals
        if (beatTimes.size() >= 4) {
            std::vector<float> intervals;
            for (size_t i = 1; i < beatTimes.size(); i++)
                intervals.push_back(beatTimes[i] - beatTimes[i - 1]);
            std::sort(intervals.begin(), intervals.end());
            float median = intervals[intervals.size() / 2];
            if (median > 0.1f) out.bpm = 60.0f / median;
        }
        out.bpm = fmaxf(60, fminf(300, out.bpm));

        del_fvec(buf);
        del_fvec(beatOut);
        del_aubio_tempo(tempo);
        del_aubio_source(src);
    }

    // ── 2. Detect onsets ──
    std::vector<float> onsets;
    {
        aubio_source_t* src = new_aubio_source(audioPath.c_str(), 0, 512);
        if (!src) return false;
        uint_t sr = aubio_source_get_samplerate(src);

        aubio_onset_t* od = new_aubio_onset("default", 512, 256, sr);
        fvec_t* buf = new_fvec(512);
        fvec_t* onsetOut = new_fvec(1);

        uint_t read = 0;
        float lastOnset = -1;
        do {
            aubio_source_do(src, buf, &read);
            aubio_onset_do(od, buf, onsetOut);
            if (onsetOut->data[0] != 0) {
                float t = aubio_onset_get_last_s(od);
                if (t - lastOnset > 0.08f) {
                    onsets.push_back(t);
                    lastOnset = t;
                }
            }
        } while (read == 512);

        del_fvec(buf);
        del_fvec(onsetOut);
        del_aubio_onset(od);
        del_aubio_source(src);
    }

    // ── 3. Map onsets to lanes ──
    float beatDur = 60.0f / out.bpm;
    int numLanes = 6;
    int laneCounter = 0;

    for (size_t i = 0; i < onsets.size(); i++) {
        float t = onsets[i];

        // Snap to nearest 1/4 beat grid
        float grid = roundf(t / (beatDur * 0.25f)) * beatDur * 0.25f;

        // Determine lane using pattern variation
        int section = (int)(t / (beatDur * 4)) % 4;
        int lane;
        switch (section) {
        case 0: lane = laneCounter % numLanes; break;
        case 1: lane = numLanes - 1 - (laneCounter % numLanes); break;
        case 2: lane = (laneCounter * 2 + 1) % numLanes; break;
        default: lane = (laneCounter * 3 + 2) % numLanes; break;
        }

        // Occasionally create hold notes
        bool makeHold = (i > 0 && (laneCounter % 7 == 0) && i + 1 < onsets.size());
        float holdEnd = makeHold ? grid + beatDur * (1 + (laneCounter % 3)) : 0;

        out.notes.push_back({grid, lane, makeHold, holdEnd});
        laneCounter++;
    }

    // Remove duplicates (same grid time + lane)
    std::sort(out.notes.begin(), out.notes.end(),
              [](const GenNote& a, const GenNote& b) {
                  return a.time < b.time || (a.time == b.time && a.lane < b.lane);
              });
    out.notes.erase(std::unique(out.notes.begin(), out.notes.end(),
                                [](const GenNote& a, const GenNote& b) {
                                    return fabsf(a.time - b.time) < 0.01f && a.lane == b.lane;
                                }),
                    out.notes.end());

    return !out.notes.empty();
}

std::string ChartGenerator::baseName(const std::string& path) {
    size_t slash = path.find_last_of("/\\");
    std::string name = (slash == std::string::npos) ? path : path.substr(slash + 1);
    size_t dot = name.find_last_of('.');
    return (dot == std::string::npos) ? name : name.substr(0, dot);
}
