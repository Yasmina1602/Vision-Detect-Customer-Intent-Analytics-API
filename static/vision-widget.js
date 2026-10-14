/**
 * VisionSearch & Analytics Embeddable Widget v2.0
 * Istalgan mavjud e-commerce saytiga (WordPress, Laravel, React, Next.js, HTML) 
 * rasm orqali qidiruv va analitika eventlarini ulash uchun universal skript.
 */

(function () {
    const currentScript = document.currentScript || document.querySelector('script[src*="vision-widget.js"]');
    const API_BASE = (currentScript && currentScript.getAttribute('data-api')) || 'http://localhost:8000';
    const SHOW_FLOATING = (currentScript && currentScript.getAttribute('data-show-floating')) !== 'false';
    const ATTACH_SELECTOR = (currentScript && currentScript.getAttribute('data-attach-to')) || null;

    // Sessiya ID yaratish yoki mavjudini olish
    let sessionId = localStorage.getItem('vision_session_id');
    if (!sessionId) {
        sessionId = 'sess_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now();
        localStorage.setItem('vision_session_id', sessionId);
    }

    let lastSearchId = null;

    // 1. Vidjet CSS stillari
    const style = document.createElement('style');
    style.innerHTML = `
        /* Suzuvchi tugma */
        .vision-floating-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            width: 56px;
            height: 56px;
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            border-radius: 50%;
            display: ${SHOW_FLOATING ? 'flex' : 'none'};
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 25px rgba(37, 99, 235, 0.45);
            cursor: pointer;
            z-index: 999998;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            border: 2px solid rgba(255, 255, 255, 0.3);
        }
        .vision-floating-btn:hover {
            transform: scale(1.1) translateY(-3px);
            box-shadow: 0 12px 30px rgba(37, 99, 235, 0.6);
        }
        .vision-floating-btn svg {
            width: 26px;
            height: 26px;
            fill: white;
        }

        /* Modal oyna */
        .vision-modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(11, 15, 25, 0.75);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            display: none;
            align-items: center;
            justify-content: center;
            z-index: 999999;
            opacity: 0;
            transition: opacity 0.25s ease;
            padding: 16px;
            box-sizing: border-box;
        }
        .vision-modal-overlay.active {
            display: flex;
            opacity: 1;
        }
        .vision-modal {
            background: #111827;
            color: #f9fafb;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 20px;
            width: 100%;
            max-width: 520px;
            max-height: 90vh;
            overflow-y: auto;
            padding: 28px;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.65);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Inter", sans-serif;
            position: relative;
            animation: visionModalPop 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
        @keyframes visionModalPop {
            from { transform: scale(0.92); opacity: 0; }
            to { transform: scale(1); opacity: 1; }
        }
        .vision-modal-close {
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: #9ca3af;
            width: 34px;
            height: 34px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }
        .vision-modal-close:hover {
            color: white;
            background: rgba(239, 68, 68, 0.2);
            border-color: rgba(239, 68, 68, 0.4);
        }
        .vision-dropzone {
            border: 2px dashed rgba(59, 130, 246, 0.4);
            border-radius: 16px;
            padding: 32px 20px;
            text-align: center;
            margin-top: 18px;
            cursor: pointer;
            background: rgba(59, 130, 246, 0.04);
            transition: all 0.2s;
        }
        .vision-dropzone:hover, .vision-dropzone.dragover {
            border-color: #3b82f6;
            background: rgba(59, 130, 246, 0.1);
            transform: scale(1.01);
        }
        .vision-samples-bar {
            margin-top: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }
        .vision-sample-chip {
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #d1d5db;
            font-size: 11px;
            padding: 5px 10px;
            border-radius: 20px;
            cursor: pointer;
            transition: all 0.15s;
            display: inline-flex;
            align-items: center;
            gap: 4px;
        }
        .vision-sample-chip:hover {
            background: rgba(59, 130, 246, 0.25);
            border-color: #3b82f6;
            color: #93c5fd;
            transform: translateY(-1px);
        }
        .vision-results-list {
            margin-top: 20px;
            display: flex;
            flex-direction: column;
            gap: 12px;
            max-height: 380px;
            overflow-y: auto;
            padding-right: 4px;
        }
        .vision-result-item {
            display: flex;
            gap: 14px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            padding: 12px;
            border-radius: 12px;
            align-items: center;
            transition: all 0.2s;
        }
        .vision-result-item:hover {
            background: rgba(255, 255, 255, 0.08);
            border-color: rgba(59, 130, 246, 0.4);
            transform: translateY(-2px);
        }
        .vision-result-img {
            width: 64px;
            height: 64px;
            border-radius: 8px;
            object-fit: cover;
            background: #1f2937;
        }
        .vision-result-info {
            flex-grow: 1;
        }
        .vision-result-title {
            font-size: 14px;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 4px;
        }
        .vision-result-price {
            color: #38bdf8;
            font-size: 13px;
            font-weight: 700;
        }
        .vision-result-btn {
            background: linear-gradient(135deg, #10b981, #059669);
            border: none;
            color: white;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            white-space: nowrap;
        }
        .vision-result-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(16, 185, 129, 0.4);
        }
        .vision-badge {
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            color: #93c5fd;
            border: 1px solid rgba(59, 130, 246, 0.3);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 12px;
            margin-right: 6px;
            margin-bottom: 6px;
        }
    `;
    document.head.appendChild(style);

    // 2. Suzuvchi kamera tugmasi
    const btn = document.createElement('div');
    btn.className = 'vision-floating-btn';
    btn.title = "AI Rasm orqali qidirish";
    btn.innerHTML = `
        <svg viewBox="0 0 24 24">
            <path d="M12 15.2a3.2 3.2 0 100-6.4 3.2 3.2 0 000 6.4z"/>
            <path d="M9 2L7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z"/>
        </svg>
    `;
    document.body.appendChild(btn);

    // 3. Modal HTML
    const modalOverlay = document.createElement('div');
    modalOverlay.className = 'vision-modal-overlay';
    modalOverlay.innerHTML = `
        <div class="vision-modal">
            <button class="vision-modal-close" id="visionCloseBtn">&times;</button>
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
                <span style="font-size:24px;">📷</span>
                <h3 style="margin:0; font-size:19px; font-weight:700; color:#fff;">Rasm orqali qidirish (AI Vision)</h3>
            </div>
            <p style="color:#9ca3af; font-size:13px; margin:0 0 14px 0; line-height:1.4;">
                Kiyimi, poyabzal yoki aksessuar rasmini yuklang — Gemini AI modelimiz uni tahlil qilib do'kondan eng o'xshash tovarlarni topadi!
            </p>
            
            <div class="vision-dropzone" id="visionDropzone">
                <div style="font-size:36px; margin-bottom:10px;">📸</div>
                <div style="font-size:14px; font-weight:600; color:#f3f4f6;">Rasmni bu yerga tashlang yoki fayl tanlang</div>
                <div style="font-size:12px; color:#9ca3af; margin-top:4px;">JPG, PNG, WEBP formatlari qo'llab-quvvatlanadi</div>
                <input type="file" id="visionFileInput" accept="image/*" style="display:none;">
            </div>

            <div style="margin-top:14px;">
                <div style="font-size:12px; color:#9ca3af; margin-bottom:6px;">💡 Yoki namunaviy rasmlarni 1 bosishda sinang:</div>
                <div class="vision-samples-bar">
                    <span class="vision-sample-chip" data-sample="https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=600" data-name="Nike Moviy Krossovka">👟 Nike Krossovka</span>
                    <span class="vision-sample-chip" data-sample="https://images.unsplash.com/photo-1576995853123-5a10305d93c0?w=600" data-name="Ko'k Jinsi Kurtka">🧥 Jinsi Kurtka</span>
                    <span class="vision-sample-chip" data-sample="https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=600" data-name="Charm Qo'l Sumkasi">👜 Charm Sumka</span>
                    <span class="vision-sample-chip" data-sample="https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=600" data-name="AirPods Max">🎧 AirPods Max</span>
                </div>
            </div>

            <div id="visionStatus" style="display:none; text-align:center; padding:20px; font-size:14px; color:#60a5fa; background:rgba(59,130,246,0.06); border-radius:12px; margin-top:15px;">
                <div style="display:inline-block; animation:spin 1s linear infinite; font-size:24px; margin-bottom:8px;">⚡</div><br>
                <span>Gemini AI rasm atributlarini tahlil qilmoqda...</span>
            </div>

            <div id="visionResults"></div>
        </div>
    `;
    document.body.appendChild(modalOverlay);

    // Modalni boshqarish
    function openModal() {
        modalOverlay.classList.add('active');
    }
    function closeModal() {
        modalOverlay.classList.remove('active');
    }

    btn.addEventListener('click', openModal);
    modalOverlay.querySelector('#visionCloseBtn').addEventListener('click', closeModal);
    modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) closeModal();
    });

    // Har qanday [data-vision-trigger] yoki #cameraSearchBtn bosilganda ochish
    document.addEventListener('click', function(e) {
        const trigger = e.target.closest('[data-vision-trigger], #cameraSearchBtn, .vision-camera-trigger');
        if (trigger) {
            e.preventDefault();
            openModal();
        }
    });

    if (ATTACH_SELECTOR) {
        const customEl = document.querySelector(ATTACH_SELECTOR);
        if (customEl) customEl.addEventListener('click', openModal);
    }

    const dropzone = modalOverlay.querySelector('#visionDropzone');
    const fileInput = modalOverlay.querySelector('#visionFileInput');
    const statusDiv = modalOverlay.querySelector('#visionStatus');
    const resultsDiv = modalOverlay.querySelector('#visionResults');

    dropzone.addEventListener('click', () => fileInput.click());
    
    // Drag & Drop
    ['dragenter', 'dragover'].forEach(name => {
        dropzone.addEventListener(name, (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    });
    ['dragleave', 'drop'].forEach(name => {
        dropzone.addEventListener(name, (e) => { e.preventDefault(); dropzone.classList.remove('dragover'); });
    });
    dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            uploadAndSearch(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            uploadAndSearch(e.target.files[0]);
        }
    });

    // Namunaviy rasmlarni 1 bosishda sinash
    modalOverlay.querySelectorAll('.vision-sample-chip').forEach(chip => {
        chip.addEventListener('click', async () => {
            const sampleUrl = chip.getAttribute('data-sample');
            const sampleName = chip.getAttribute('data-name');
            statusDiv.style.display = 'block';
            statusDiv.innerHTML = `<span>'${sampleName}' namunaviy rasmi yuklanmoqda va AI tahliliga yuborilmoqda...</span>`;
            resultsDiv.innerHTML = '';
            dropzone.style.display = 'none';

            try {
                const response = await fetch(sampleUrl);
                const blob = await response.blob();
                const file = new File([blob], "sample.jpg", { type: blob.type || "image/jpeg" });
                await uploadAndSearch(file);
            } catch (err) {
                statusDiv.innerHTML = `<span style="color:#ef4444;">Rasmni yuklashda xatolik: ${err.message}</span>`;
                dropzone.style.display = 'block';
            }
        });
    });

    // 4. API ga rasm yuborish
    async function uploadAndSearch(file) {
        statusDiv.style.display = 'block';
        statusDiv.innerHTML = `<span>⚡ Gemini AI rasmni tahlil qilmoqda...</span>`;
        resultsDiv.innerHTML = '';
        dropzone.style.display = 'none';

        const formData = new FormData();
        formData.append('file', file);
        formData.append('session_id', sessionId);

        try {
            const res = await fetch(`${API_BASE}/api/v1/visual-search`, {
                method: 'POST',
                body: formData
            });

            const data = await res.json();
            if (!res.ok) throw new Error(data.detail || 'Xatolik yuz berdi');

            lastSearchId = data.search_id;
            statusDiv.style.display = 'none';
            dropzone.style.display = 'block';

            renderResults(data);
        } catch (err) {
            statusDiv.innerHTML = `<span style="color:#ef4444;">Xatolik: ${err.message}</span>`;
            dropzone.style.display = 'block';
        }
    }

    // 5. Natijalarni chizish
    function renderResults(data) {
        const detected = data.ai_detected;
        let html = `
            <div style="margin-top:16px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); padding:12px; border-radius:12px;">
                <div style="font-size:12px; color:#9ca3af; margin-bottom:6px;">AI Aniqlagan Atributlar:</div>
                <span class="vision-badge">🔍 ${detected.search_query || detected.category}</span>
                <span class="vision-badge">📂 ${detected.category || 'Noma\'lum'}</span>
                <span class="vision-badge">🎨 ${detected.color || 'Aralash'}</span>
                <span class="vision-badge" style="background:rgba(16, 185, 129, 0.2); color:#6ee7b7; border-color:rgba(16,185,129,0.3);">⚡ Model: ${data.model_used || 'Gemini'}</span>
            </div>
        `;

        if (!data.products || data.products.length === 0) {
            html += `
                <div style="padding:16px; background:rgba(239,68,68,0.1); border:1px solid rgba(239,68,68,0.25); border-radius:12px; margin-top:14px; font-size:13px; text-align:center; color:#fca5a5;">
                    ⚠️ Do'konda ayni damda aynan bunday tovar topilmadi.<br>
                    <b>Marketologlarga talab qayd etildi!</b> Tez orada olib kelinishi mumkin.
                </div>
            `;
        } else {
            html += `
                <div style="margin-top:14px; font-size:13px; font-weight:600; color:#93c5fd;">
                    Topilgan mos mahsulotlar (${data.products.length} ta):
                </div>
                <div class="vision-results-list">
            `;
            data.products.forEach(item => {
                const p = item.product;
                const matchPct = Math.round(item.match_score * 100);
                html += `
                    <div class="vision-result-item">
                        <img src="${p.image_url || 'https://via.placeholder.com/64'}" class="vision-result-img" alt="${p.name}">
                        <div class="vision-result-info">
                            <div class="vision-result-title">${p.name}</div>
                            <div class="vision-result-price">$${p.price} <span style="color:#10b981; font-size:11px; font-weight:normal;">(${matchPct}% moslik)</span></div>
                        </div>
                        <button class="vision-result-btn" onclick="window.VisionAnalytics.track('ADD_TO_CART', ${p.id}, '${p.name}')">Savatga</button>
                    </div>
                `;
            });
            html += `</div>`;
        }

        resultsDiv.innerHTML = html;
    }

    // 6. Global Ob'yektlar
    window.VisionWidget = {
        open: openModal,
        close: closeModal,
        searchImage: uploadAndSearch
    };

    window.VisionAnalytics = {
        track: async function (eventType, productId = null, productName = "") {
            // A) Meta Pixel agar saytda bo'lsa
            if (typeof fbq === 'function') {
                fbq('track', eventType, { content_ids: productId ? [productId] : [] });
            }

            // B) Shaxsiy backendga yuborish
            try {
                await fetch(`${API_BASE}/api/v1/track-event`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        session_id: sessionId,
                        search_id: lastSearchId,
                        product_id: productId,
                        event_type: eventType
                    })
                });
                console.log(`[VisionAnalytics] Event yuborildi: ${eventType} (Product: ${productId})`);
                
                // Saytda maxsus hodisa chiqarish
                window.dispatchEvent(new CustomEvent('vision:event_tracked', {
                    detail: { eventType, productId, productName }
                }));

                if (productName && eventType === 'ADD_TO_CART') {
                    // Agar maxsus toast bo'lmasa oddiy alert
                    if (typeof window.showStoreToast === 'function') {
                        window.showStoreToast(`'${productName}' savatga qo'shildi!`);
                    }
                }
            } catch (e) {
                console.error('[VisionAnalytics] Xatolik:', e);
            }
        }
    };

    console.log('[VisionWidget] Versiya 2.0 muvaffaqiyatli ishga tushdi!');
})();
