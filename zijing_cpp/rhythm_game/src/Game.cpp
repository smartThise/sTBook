#include "Game.h"
#include "FilePicker.h"
#include <cmath>
#include <cstring>
#include <algorithm>

void Game::run() {
    InitWindow(Config::SW, Config::SH, "Rhythm Game");
    InitAudioDevice();
    SetTargetFPS(60);

    audio_.init();
    renderer_.init();
    songMgr_.scanSongs();

    while (!WindowShouldClose()) {
        float dt = GetFrameTime();
        bgPhase_ += dt * 0.5f;
        audio_.updateMusic();

        switch (state_) {
        case GameState::MENU:     tickMenu(); break;
        case GameState::SELECT:   tickSelect(); break;
        case GameState::IMPORTING: tickImporting(); break;
        case GameState::PLAYING:  tickPlaying(dt); break;
        case GameState::RESULT:   tickResult(); break;
        }
    }

    renderer_.shutdown();
    audio_.cleanup();
    CloseWindow();
}

void Game::startGame() {
    state_ = GameState::PLAYING;
    gameTime_ = 0;
    memset(laneFlash_, 0, sizeof(laneFlash_));
    comboScale_ = 1; screenFlash_ = 0; beatPulse_ = 0;
    lastJudgeTime_ = -1; lastJudge_ = JudgeResult::NONE;
    judge_.reset();
    particles_.clear();

    audio_.stopMusic();

    if (!chart_.loadFromFile(chartPath_))
        chart_.generate();

    // Load and play background music
    std::string ap;
    for (auto& s : songMgr_.songs()) {
        if (s.filePath == chartPath_) { ap = s.audioPath; break; }
    }
    if (ap.empty()) ap = songMgr_.audioPathFor({"", chartPath_, 0, ""});
    printf("[DEBUG] startGame: chartPath=%s audioPath=%s\n", chartPath_.c_str(), ap.c_str());
    if (!ap.empty() && audio_.loadMusic(ap)) {
        printf("[DEBUG] loadMusic OK, playing...\n");
        audio_.playMusic();
    } else {
        printf("[DEBUG] no music loaded\n");
    }

    audio_.resetBeat();
}

void Game::tickMenu() {
    renderer_.beginFrame();
    renderer_.drawMenu(bgPhase_);
    renderer_.endFrame();
    if (input_.enterPressed()) {
        state_ = GameState::SELECT;
        selectedSong_ = 0;
        selectScroll_ = 0;
        selectJustEntered_ = true;
    }
}

void Game::tickSelect() {
    if (selectJustEntered_) {
        selectJustEntered_ = false;
        renderer_.beginFrame();
        renderer_.drawSelect(bgPhase_, songMgr_.songs(), selectedSong_, selectScroll_,
                             true);
        renderer_.endFrame();
        return;
    }

    if (input_.escapePressed()) { state_ = GameState::MENU; return; }

    // Import key (I key)
    if (IsKeyPressed(KEY_I)) {
        state_ = GameState::IMPORTING;
        importStatus_ = "";
        importProgress_ = 0;
        return;
    }

    if (IsKeyPressed(KEY_UP) || IsKeyPressed(KEY_W)) {
        selectedSong_ = (selectedSong_ - 1 + (int)songMgr_.songs().size()) % (int)songMgr_.songs().size();
    }
    if (IsKeyPressed(KEY_DOWN) || IsKeyPressed(KEY_S)) {
        selectedSong_ = (selectedSong_ + 1) % (int)songMgr_.songs().size();
    }
    selectScroll_ += (selectedSong_ * 70.0f - selectScroll_) * 0.2f;

    if (input_.enterPressed()) {
        chartPath_ = songMgr_.songs()[selectedSong_].filePath;
        startGame();
        return;
    }

    renderer_.beginFrame();
    renderer_.drawSelect(bgPhase_, songMgr_.songs(), selectedSong_, selectScroll_, true);
    renderer_.endFrame();
}

void Game::tickImporting() {
    // Show progress UI
    renderer_.beginFrame();
    renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
    renderer_.endFrame();

    // First frame: open file dialog
    if (importStatus_.empty()) {
        importStatus_ = "Opening file dialog...";
        importProgress_ = 0.1f;
        renderer_.beginFrame();
        renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
        renderer_.endFrame();

        std::string path = openAudioFileDialog();
        if (path.empty()) {
            importStatus_ = "Cancelled. Press any key...";
            importProgress_ = -1;
            return;
        }

        importStatus_ = "Analyzing audio...";
        importProgress_ = 0.3f;
        renderer_.beginFrame();
        renderer_.drawImport(bgPhase_, importStatus_.c_str(), importProgress_);
        renderer_.endFrame();

        std::string outChart;
        if (songMgr_.importAudio(path, outChart)) {
            importStatus_ = "Import complete! Press ENTER.";
            importProgress_ = 1.0f;
            songMgr_.scanSongs();
            // Find and select the newly imported song
            auto& songs = songMgr_.songs();
            for (size_t i = 0; i < songs.size(); i++) {
                if (songs[i].filePath == outChart) {
                    selectedSong_ = (int)i;
                    break;
                }
            }
        } else {
            importStatus_ = "Import failed! Press any key.";
            importProgress_ = -1;
        }
        return;
    }

    // Waiting for user to dismiss
    if (importProgress_ >= 1.0f) {
        if (input_.enterPressed()) {
            selectJustEntered_ = true;
            state_ = GameState::SELECT;
        }
    } else if (importProgress_ < 0) {
        if (input_.enterPressed() || input_.escapePressed()) {
            selectJustEntered_ = true;
            state_ = GameState::SELECT;
        }
    }
}

void Game::tickResult() {
    renderer_.beginFrame();
    renderer_.drawResults(bgPhase_, judge_.score(), judge_.maxCombo(),
                          std::array<int,4>{judge_.count(JudgeResult::PERFECT),
                                            judge_.count(JudgeResult::GREAT),
                                            judge_.count(JudgeResult::GOOD),
                                            judge_.count(JudgeResult::MISS)}.data(),
                          chart_.size());
    renderer_.endFrame();
    if (input_.enterPressed()) state_ = GameState::MENU;
}

void Game::tickPlaying(float dt) {
    audio_.updateMusic();
    gameTime_ += dt;

    float pulse = audio_.updateBeat(gameTime_);
    if (pulse > 0) beatPulse_ = pulse;

    for (int i = 0; i < Config::LANES; i++)
        laneFlash_[i] *= powf(0.005f, dt);
    comboScale_ = fmaxf(1, comboScale_ + (1 - comboScale_) * (1 - powf(0.02f, dt)));
    screenFlash_ *= powf(0.01f, dt);
    beatPulse_ *= powf(0.02f, dt);

    particles_.update(dt);

    for (size_t i = 0; i < chart_.size(); i++) {
        Note& n = chart_.note(i);
        if (n.result != JudgeResult::NONE) continue;
        if (n.type == NoteType::TAP && gameTime_ > n.time + Config::JW_GOOD) {
            n.result = JudgeResult::MISS;
            judge_.apply(JudgeResult::MISS);
            lastJudge_ = JudgeResult::MISS;
            lastJudgeTime_ = gameTime_;
        } else if (n.type == NoteType::HOLD && gameTime_ > n.time + Config::JW_GOOD) {
            n.result = JudgeResult::MISS;
            n.holdResult = JudgeResult::MISS;
            judge_.applyHold(JudgeResult::MISS, JudgeResult::MISS);
            lastJudge_ = JudgeResult::MISS;
            lastJudgeTime_ = gameTime_;
        }
    }

    for (size_t i = 0; i < chart_.size(); i++) {
        Note& n = chart_.note(i);
        if (n.type != NoteType::HOLD || !n.holding || n.holdResult != JudgeResult::NONE) continue;
        if (gameTime_ >= n.endTime) {
            float tailDiff = fabsf(gameTime_ - n.endTime);
            JudgeResult tailJ = judge_.judge(tailDiff);
            if (tailJ == JudgeResult::NONE) tailJ = JudgeResult::GOOD;
            n.holdResult = tailJ;
            n.holding = false;
            judge_.applyHold(n.result, tailJ);
            comboScale_ = 1.5f;
            if (tailJ == JudgeResult::PERFECT) screenFlash_ = 0.5f;
            float hx = Config::FIELD_X + (n.lane + 0.5f) * Config::LANE_W;
            particles_.spawnExplosion(hx, Config::HIT_Y, n.lane);
        }
    }

    for (int lane : input_.pressedLanes()) {
        laneFlash_[lane] = 1;
        Note* best = nullptr;
        float bd = 999;
        for (size_t i = 0; i < chart_.size(); i++) {
            Note& n = chart_.note(i);
            if (n.lane != lane || n.result != JudgeResult::NONE) continue;
            float d = fabsf(gameTime_ - n.time);
            if (d < bd && d < Config::JW_GOOD) { best = &n; bd = d; }
        }
        if (best) {
            JudgeResult j = judge_.judge(bd);
            best->result = j;
            if (best->type == NoteType::HOLD) {
                best->holding = true;
            }
            judge_.apply(j);
            comboScale_ = 1.8f;
            lastJudge_ = j;
            lastJudgeTime_ = gameTime_;
            if (j == JudgeResult::PERFECT) screenFlash_ = 1;

            audio_.playLane(lane);
            float hx = Config::FIELD_X + (lane + 0.5f) * Config::LANE_W;
            particles_.spawnExplosion(hx, Config::HIT_Y, lane);
            particles_.spawnSpiral(hx, Config::HIT_Y, gameTime_, lane);
            if (judge_.combo() > 10) particles_.spawnFire(hx, Config::HIT_Y);
        }
    }

    for (int lane : input_.releasedLanes()) {
        Note* activeHold = nullptr;
        for (size_t i = 0; i < chart_.size(); i++) {
            Note& n = chart_.note(i);
            if (n.type == NoteType::HOLD && n.lane == lane && n.holding && n.holdResult == JudgeResult::NONE) {
                activeHold = &n;
                break;
            }
        }
        if (activeHold) {
            float tailDiff = fabsf(gameTime_ - activeHold->endTime);
            JudgeResult tailJ = tailDiff < Config::JW_GOOD ? judge_.judge(tailDiff) : JudgeResult::MISS;
            activeHold->holdResult = tailJ;
            activeHold->holding = false;
            judge_.applyHold(activeHold->result, tailJ);
            comboScale_ = 1.5f;
            if (tailJ == JudgeResult::PERFECT) screenFlash_ = 0.5f;
            lastJudge_ = tailJ;
            lastJudgeTime_ = gameTime_;
            float hx = Config::FIELD_X + (lane + 0.5f) * Config::LANE_W;
            particles_.spawnExplosion(hx, Config::HIT_Y, lane);
        }
    }

    if (input_.escapePressed()) { audio_.stopMusic(); state_ = GameState::MENU; return; }
    if (chart_.allDone()) { audio_.stopMusic(); state_ = GameState::RESULT; return; }

    for (int i = 0; i < Config::LANES; i++)
        keysDown_[i] = input_.isKeyDown(i);

    float progress = chart_.size() > 0 ? (float)chart_.doneCount() / (float)chart_.size() : 1;

    renderer_.beginFrame();
    renderer_.drawBackground(bgPhase_, dt);
    renderer_.drawTrackBase(beatPulse_);
    renderer_.drawLanes(laneFlash_, beatPulse_);
    renderer_.drawBeatLines(gameTime_);
    renderer_.drawNotes(chart_.notes(), gameTime_);
    renderer_.drawHitLine(beatPulse_, laneFlash_);
    renderer_.drawReceptors(laneFlash_, keysDown_);
    renderer_.drawParticles(particles_.particles());
    renderer_.drawScreenFlash(screenFlash_);
    renderer_.drawJudgment(lastJudge_, gameTime_ - lastJudgeTime_);
    renderer_.drawUI(judge_.score(), judge_.combo(), comboScale_, progress);
    renderer_.endFrame();
}
