# Noah Infinite Universe Web App  
**October 2023 – December 2023**  

> “We are all scattered stardust—and Noah gathers those particles into brilliant constellations.”  
> With Noah Infinite Universe, your face becomes the ink, and the cosmos becomes the pen, painting an epic that’s uniquely yours.  
<img width="1232" alt="eb4857a235bbd58d054e5fe673cddd6" src="https://github.com/user-attachments/assets/37ea1342-703d-4350-a826-b0f305d82f0c" />

---

## 🚀 Project Overview  
Noah Infinite Universe is a Django web application that harnesses cutting-edge AI to generate a 20-panel “comic strip” starring you. Simply upload **5 personal photos**, enter your desired story theme, and watch a Vue 3 + TypeScript frontend talk to the backend via WebSocket in real-time—then deliver a fully AI-crafted, high-fidelity narrative in images.  

## ✨ Key Features  
1. **Personalized Style Transfer**  
   - Fine-tune personalized face embeddings on your five uploaded photos using our proprietary face-swap network enhanced with LoRA (Low-Rank Adaptation) 
   - Leverage an optimized inference engine to deliver ultra-realistic swaps in seconds, complete with real-time previews of your creative results 

2. **Real-Time Progress & Interaction**  
   - Vue 3 + TypeScript SPA communicates over WebSocket  
   - Live progress indicators for queue position, generation status, and instant previews  

3. **Scalable, Distributed Backend**  
   - **API Layer**: Django REST Framework  
   - **Data Storage**: PostgreSQL for user profiles and task metadata  
   - **Task Queue**: Celery + RabbitMQ  
   - **Cache**: Redis for intermediate results  

4. **AI Pipeline & Deployment**  
   - **Image Generation**: Dockerized EasyFace (Stable Diffusion + ControlNet)  
   - **Scripted Prompts**: GLM3 local service splits story text into 20 prompts  
   - **Reverse Proxy & Security**: Nginx + HTTPS  
   - **Monitoring**: Prometheus + Grafana for uptime and performance  

## ⚙️ Installation & Run  

1. **Clone the repository**  
   ```bash
   git clone https://github.com/leinusi/Noah-Infinite-Universe.git
   cd Noah-Infinite-Universe
2. **Start the backend server**  
   ```bash
   cd NoahAI_web_serve
   python manage.py runserver 6006
## 📖 How to Use  
1. **Upload Photos**  
   Click “Upload” and select five clear personal shots (frontal or profiles).  
2. **Enter a Theme**  
   In the theme input box, type in the narrative you’d like. For example:  
   - “I want to generate a story where I’m the Empress in a Qing Dynasty palace.”  
   - “I’m a top agent infiltrating a Nazi camp to complete a mission.” 
3. **Generate Your Comic**  
   Hit “Generate,” watch the live progress bar, and preview frames as they appear.
<img width="1231" alt="4c4f6ce71cb773578d15bffa7a69a05" src="https://github.com/user-attachments/assets/4fd01db5-3f4d-4256-84fe-0b62de697a20" />

5. **Download & Share**  
   When all 20 frames are ready, download them as a ZIP or share directly to social platforms.  

## 🔮 Future Roadmap  
- **Multi-Scene Storylines**: Seamlessly link different themes into a continuous timeline  
- **Social Integration**: One-click sharing to WeChat, Weibo, Instagram  
- **Enhanced Model Training**: Scale up LoRA clusters and add more ControlNet variants for even richer detail
<img width="1230" alt="ba6f3d7719349c6b9e106cea59577fe" src="https://github.com/user-attachments/assets/88c00679-4c6d-4c2b-829c-b83fda31b1b0" />

---  

Noah Infinite Universe is more than a web app—it’s your personalized, limitless narrative. Ready to write your own legend? 🌟  


   
