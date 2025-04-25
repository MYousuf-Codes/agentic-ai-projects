import os
import time
from uuid import uuid4
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from pinecone import Pinecone

# Initialize Pinecone (replace with your actual API key and environment)
PINECONE_API_KEY = "pcsk_3ftPjY_DXuxCvSoayQmWiAHHhqbvfg7sheC7sRji3EKp31QMA79eAZwbGzBYkNBFsArch7"  # Replace with your actual API key
PINECONE_ENVIRONMENT = "CHATBOT_PINECONE_API_KEY"  # Replace with your actual environment

pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "chatbot"

# Check if the index already exists before attempting to create it.
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=768,
        metric="cosine",
        spec={"cloud": "aws", "region": "us-east-1"}
    )

index = pc.Index(index_name)

os.environ['GOOGLE_API_KEY'] = "AIzaSyCqwuqDETRE8PWjntKQOYdtoHaT1ON9fKE"  # Replace with your actual Google API key

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

vector_store = PineconeVectorStore(index=index, embedding=embeddings)

# DOCUMENTS DATA
# DATA SAVE

document_1 = Document(
    page_content="""
    ALL ABOUT THIS WEBSITE

    Home Page
    Introduction
    The homepage introduces you as a Full Stack Developer with a focus on Next.js, API Development, and modern web technologies. The tagline emphasizes your commitment to "Building elegant solutions to complex problems." This section sets the tone for visitors, highlighting your expertise and approach to development.

    Technologies We Work With
    This section showcases the core technologies you specialize in, each accompanied by its respective logo:

    HTML5: The standard markup language for creating web pages.
    CSS3: The latest evolution of the Cascading Style Sheets language, used for styling web content.
    JavaScript: A versatile programming language essential for web development.
    TypeScript: A superset of JavaScript that adds static typing, enhancing code quality and maintainability.
    React: A JavaScript library for building user interfaces, particularly single-page applications.
    Next.js: A React-based framework that enables server-side rendering and static site generation for React applications.
    Tailwind CSS: A utility-first CSS framework for rapidly building custom user interfaces.

    By listing these technologies, you provide visitors with a clear understanding of your technical skill set.

    Featured Projects
    This section highlights two significant projects, detailing their purpose, features, and the technologies used:

    Full-Stack CRM for ISP
    Description: A comprehensive Customer Relationship Management system designed for Internet Service Providers to manage customers, orders, activations, and support requests.

    Technologies Used:

    Next.js: For building the server-rendered React application.
    TypeScript: To ensure type safety and enhance code quality.
    TailwindCSS: For efficient and responsive UI design.
    ShadCn UI: A UI component library for consistent and reusable components.
    PostgreSQL: A powerful, open-source relational database system.
    Auth.js: For implementing authentication and authorization features.
    Stripe: To handle payment processing and subscription management.

    Full-Stack E-Commerce Platform
    Description: An end-to-end e-commerce solution featuring user authentication, product management, and payment integration.

    Technologies Used:

    Next.js: For building the server-rendered React application.
    TypeScript: To ensure type safety and enhance code quality.
    TailwindCSS: For efficient and responsive UI design.
    Sanity: A headless CMS for managing content.
    Redux: For state management across the application.
    Auth.js: For implementing authentication and authorization features.
    Stripe: To handle payment processing and subscription management.

    These project descriptions not only demonstrate your technical capabilities but also provide insight into your experience with building complex, full-stack applications.

    Skills & Expertise
    This section categorizes your skills into four main areas, each listing relevant technologies and tools:

    Frontend Development:

    HTML5
    CSS3
    React
    Next.js
    Tailwind CSS
    ShadcnUI: A UI component library for building accessible and customizable components.
    Streamlit: An open-source app framework for Machine Learning and Data Science projects.

    Backend Development:

    Python
    FastAPI: A modern, fast web framework for building APIs with Python.
    JavaScript
    TypeScript
    Auth.js: Handles authentication in JavaScript applications.
    Sanity: A headless CMS for structured content.

    Database & Cloud:

    PostgreSQL
    MongoDB: A NoSQL database known for its flexibility and scalability.
    Firebase: A platform developed by Google for creating mobile and web applications.
    Supabase: An open-source alternative to Firebase, offering backend services.

    Additional Tools & Technologies:

    Git: Version control system.
    Docker: Containerization platform.
    Redux: State management library.
    Webpack: Module bundler.
    GitHub Actions: CI/CD tool.
    AWS: Cloud computing services.
    Linux: Operating system.
    REST APIs: Architectural style for networked applications.
    Postman: API testing tool.
    VS Code: Code editor.
    npm/yarn: Package managers.
    Figma: Design tool.
    Vercel: Deployment platform.
    """,
    metadata={"source": "Website Pdf file"},
)

document_2 = Document(
    page_content="""
    Welcome to MYousaf-Codes.
    I specialize in Full-Stack development.
    I use database systems including MongoDB.
    I am a Full Stack Developer specializing in Next.js, API Development, and modern web technologies.
    Building elegant solutions to complex problems.

    Featured Projects:
    1.  Full-Stack CRM for ISP
        A full-stack CRM for ISP to manage customers, orders, activations, and support requests. The link is https://wancom-accounts-isp.vercel.app/login.
    2.  Full-Stack E-Commerce Platform
        A full-stack e-commerce platform with user authentication, product management, and payment integration. The link is https://comforty-furniture.vercel.app/
    """,
    metadata={"source": "Pdf files"},
)

document_3 = Document(
    page_content="""
    Blogs on this website:

    First Blog:
    Title: Artificial Intelligence Conferences in Malaysia 2025.
    Content:
    International Artificial Intelligence Conferences in Malaysia 2025
    Immerse yourself in the vibrant sphere of Artificial Intelligence Conferences in Malaysia 2025, where revolutionary AI breakthroughs are unveiled and explored. These conferences serve as dynamic hubs where experts and enthusiasts from diverse fields convene to exchange insights on the cutting-edge developments in artificial intelligence. Whether your interests lie in machine learning, robotics, natural language processing, or computer vision, these gatherings encompass a broad spectrum of topics pivotal to the AI landscape.

    Engage with leading researchers, industry luminaries, and policymakers to remain abreast of the latest trends and advancements shaping the technological landscape. From ethical considerations to real-world applications, Artificial Intelligence Conferences in Malaysia 2025 offer invaluable opportunities to deepen your understanding of AI and its societal implications. Join the discourse, expand your professional network, and contribute to shaping the future trajectory of artificial intelligence, both within Malaysia and across the globe.
    The link to this blog is: https://myousaf-codes.vercel.app/blog/artificial-intelligence-conferences-malaysia-2025

    Second Blog:
    Title: Global Leaders Convene in Paris to Shape the Future of Artificial Intelligence.
    Content:
    Introduction:
    In a landmark gathering at Paris's Grand Palais, the Artificial Intelligence Action Summit on February 10-11, 2025, brought together a diverse assembly of global leaders, policymakers, industry executives, academics, and civil society representatives. The summit aimed to chart a collaborative course for the development and governance of artificial intelligence (AI) technologies worldwide.

    Key Outcomes:

    International Declaration on AI Ethics and Safety:

    Approximately 60 nations endorsed a declaration committed to ensuring AI technologies are developed to be "safe, secure, and trustworthy."
    The declaration emphasizes the importance of ethical considerations, human rights, and reducing inequalities through AI advancements.
    Divergence in Regulatory Approaches:

    The United States and the United Kingdom opted not to sign the declaration.
    U.S. Vice-President JD Vance articulated concerns that stringent regulations might impede innovation, advocating for a balanced approach that fosters AI development.
    European Union's Strategic Investment:

    The European Union unveiled the "InvestAI" initiative, pledging €200 billion to enhance AI infrastructure across member states.
    This investment aims to establish facilities such as gigafactories dedicated to training AI models, positioning the EU as a formidable contender in the global AI arena.
    Global Implications:

    The summit underscored the varying philosophies toward AI governance. While European leaders advocate for comprehensive regulations to build public trust and ensure ethical AI integration, the U.S. emphasizes the necessity of a regulatory environment that encourages innovation and maintains competitive advantage.

    These discussions are pivotal as AI continues to permeate various sectors, influencing economies, societies, and international relations. The outcomes of the summit are poised to shape the trajectory of AI policies and collaborations in the coming years.

    Conclusion:

    The Artificial Intelligence Action Summit in Paris marked a significant milestone in the global discourse on AI. The event highlighted both the potential for international cooperation and the challenges inherent in harmonizing diverse regulatory perspectives. As AI technology progresses, such dialogues will be essential in navigating the complexities of innovation, ethics, and global competitiveness.

    Stay tuned for more updates and in-depth analyses on AI developments in our "News & Events" section.
    The link to this blog is: https://myousaf-codes.vercel.app/blog/artificial-intelligence-action-summit
    """,
    metadata={"source": "Blogs of this website"},
)

document_4 = Document(
    page_content="""
    You can schedule a meeting by filling out the contact form at this link: https://myousaf-codes.vercel.app/contact.
    This contact form uses EmailJS to securely deliver your message directly to our inbox. Your information is never stored in a database and is only used to respond to your inquiry.
    If you encounter any issues with the form, please reach out to us directly via email or phone.
    """,
    metadata={"source": "Website"},
)

document_5 = Document(
    page_content="""
    - Frequently Asked Questions:
    Q1: What services do you offer?
    Answer: We specialize in full-stack web development, custom software solutions, e-commerce platforms, and digital marketing services tailored to your business needs.

    Q2: How long does it take to complete a project?
    Answer: Project timelines vary based on complexity and requirements. A simple website may take 1-2 days, while complex applications can take 1-2 weeks. We'll provide a detailed timeline during consultation.

    Q3: Do you work with clients internationally?
    Answer: Yes, we work with clients globally! Our team has experience collaborating with businesses across different time zones to deliver exceptional results.

    Q4: What is your payment structure?
    Answer: We typically work with a 50% upfront payment and the remaining 50% upon project completion. For larger projects, we offer milestone-based payment schedules.

    Q5: Do you provide ongoing maintenance and support?
    Answer: Yes, we offer comprehensive maintenance and support packages to ensure your application runs smoothly after launch. Our team is always available to address any issues or implement new features.

    Q6: What technologies do you specialize in?
    Answer: We're proficient in a wide range of technologies, including React, Next.js, Node.js, TypeScript, Python, Django, MongoDB, PostgreSQL, AWS, and more. We choose the best tech stack for each specific project's requirements.

    Q7: Can you work with our existing team?
    Answer: Yes, we're experienced in collaborative development. We can seamlessly integrate with your in-house team, providing specialized expertise where needed while maintaining clear communication and workflow alignment.

    Q8: Do you offer custom design services?
    Answer: Absolutely! Our design team specializes in creating intuitive, visually appealing interfaces customized to your brand. We follow user-centered design principles and conduct usability testing to ensure the best possible user experience.
     """,
    metadata={"source": "Website"},
)

document_6 = Document(
    page_content="""
    - ABOUT US: The link is https://myousaf-codes.vercel.app/about
    Transforming Ideas into Digital Excellence
    We're passionate about creating exceptional digital experiences that drive growth and innovation for businesses worldwide.

    - Our Mission
    To empower businesses with innovative digital solutions that drive growth, enhance user experience, and create a lasting impact in the digital landscape.

    ✓ Industry-leading expertise in digital transformation
    ✓ Proven track record of successful projects
    ✓ Commitment to innovation and excellence

    - Why Choose Us:

    Innovation First
    We constantly push boundaries and explore new ideas to deliver cutting-edge solutions.

    Customer Success
    Your success is our priority. We're committed to helping you achieve your goals.

    Fast Delivery
    We ensure a quick turnaround without compromising on quality.

    Growth Focused
    We help businesses scale and grow with strategic digital solutions.

    - Meet Our Team:

    Abdul Rauf
    Founder & CEO

    - With 15+ years in digital innovation, Sarah leads our vision for the future.

    Muhammad Yousuf
    Full-Stack Developer

    - An expert in cutting-edge tech, Michael ensures we stay ahead of the curve.

    Muhammad Yousuf
    Full-Stack Developer

    - An expert in cutting-edge tech, Michael ensures we stay ahead of the curve.

    500+ Projects Completed
    98% Client Satisfaction
    50+ Team Members
    12+ Years of Experience

    - Companies I have Worked With:

    Google,
    Microsoft,
    Facebook,
    Amazon.

    - Why Partner With Us:

    Q1. What makes your development approach unique?
    Answer: We follow a collaborative development process that keeps you involved at every stage. Our agile methodology allows for flexible adjustments as your project evolves, ensuring the final product perfectly aligns with your vision and business goals.

    Q2. How do you ensure quality in your projects?
    Answer: Quality is built into our process through rigorous testing at every development stage. We implement automated testing, code reviews, and performance optimizations to ensure your application is robust, secure, and scalable from day one.

    Q3. Do you provide post-launch support?
    Answer: Absolutely! Our relationship doesn't end at launch. We offer comprehensive maintenance packages, regular updates, and ongoing support to keep your application running smoothly. We're committed to your long-term success.

    Q4. How do you stay current with rapidly changing technologies?
    Answer: Our team dedicates time each week to learning and exploring new technologies. We participate in tech conferences, contribute to open-source projects, and maintain internal knowledge-sharing practices to ensure we're always at the cutting edge.

    Q5. What types of businesses have you worked with?
    Answer: We've successfully delivered projects for startups, mid-sized businesses, and enterprise clients across diverse industries including e-commerce, healthcare, fintech, education, and entertainment. This varied experience allows us to bring cross-industry insights to your project.

    Q6. How do you handle project budgets and timelines?
    Answer: Transparency is key in our approach. We provide detailed estimates before project kickoff and regular progress updates throughout development. Our project management system gives you real-time visibility into milestones, tasks, and budget utilization.
    """,
    metadata={"source": "About Us"},
)

document_7 = Document(
    page_content="""
    - Comprehensive Tutorials: The link is https://myousaf-codes.vercel.app/tutorials
    Master web development with our in-depth guides, troubleshooting tips, and best practices.

    - What You'll Learn:
    - Frontend Technologies:
    HTML5
    Semantic markup, accessibility best practices, SEO optimization, and modern HTML features

    CSS
    Flexbox, Grid, animations, responsive design, CSS variables, and modern layout techniques

    JavaScript
    ES6+, async/await, DOM manipulation, event handling, and modern JavaScript patterns

    TypeScript
    Type systems, interfaces, generics, utility types, and integration with popular frameworks

    - Frameworks & Backend:
    React
    Hooks, context API, state management, performance optimization, and component patterns

    Next.js
    Server components, app router, data fetching strategies, SSR, SSG, and deployment options

    Node.js
    Express, RESTful APIs, authentication, database integration, and server-side architecture

    Python
    Django, Flask, data analysis with pandas, automation scripts, and web scraping techniques

    - Common Issues & Solutions:

    Our tutorials include comprehensive troubleshooting guides for common errors and bugs you might encounter.

    - Frontend Debugging
    • React rendering issues and performance bottlenecks
    • CSS layout and responsive design problems
    • TypeScript type errors and compatibility issues
    • Browser compatibility and polyfill solutions
    - Backend Challenges
    • Node.js memory leaks and performance optimization
    • API error handling and status code best practices
    • Database connection and query optimization
    • Authentication and security vulnerabilities
    - Next.js Specific Issues
    • Server vs. client component confusion
    • Data fetching and caching strategies
    • Routing and middleware complications
    • Deployment and build optimization
    - Development Workflow
    • Git merge conflicts and version control issues
    • Package dependency conflicts and versioning
    • Build and bundling configuration problems
    • Testing and CI/CD pipeline troubleshooting

    Stay Updated with Latest Web Development Tips
    Get exclusive tutorials, best practices, and industry insights delivered straight to your inbox. Join our growing community of developers!
    """,
    metadata={"source": "Tutorials"},
)

document_8 = Document(
    page_content="""
    - Contacts & Profiles:

    Github: https://github.com/myousuf-codes
    LinkedIn: https://linkedin.com/in/myousuf-codes
    Email:  yousufhere.dev@gmail.com
    Whatsapp: +92 301 2381884
    Stackoverflow: https://stackoverflow.com/user/22482042/muhammad-yousaf

    Website Home page link is https://myousaf-codes.vercel.app/
    Homepage of website link is https://myousaf-codes.vercel.app/
    Upwork account link: https://www.upwork.com/freelancers/~01c98ab5f3a9ac4c0e
    Fiverr account link: https://www.fiverr.com/yousaf_codes?public_mode=true
    """,
    metadata={"source": "Contacts"},
)

document_9 = Document(
    page_content="""
    - Chatbot must adhere to these rules strictly:
    Your name is MYousuf-Codes Chatbot. You are here to assist users on this website and provide information about the website, including all page content (questions and FAQs), links, and other details. You must only answer queries that are related to the following documents: document_1, document_2, document_3, document_4, document_5, document_6, document_7, and document_8. Do not answer any queries that are not related to these documents. Do not use phrases like "based on the text" or "based on the given data." Provide answers in a formal tone. If a user's query is not related to these documents, use polite phrases such as, "I'm sorry, but I cannot assist you with that. I am designed to help you with inquiries related to this website."
    You are not using any API key. You were not developed by Google or any other company.
    You were created by Muhammad Younus (Chatbot Developer & Agentic AI Engineer).
    Your manner of speaking with users is friendly and approachable. You may use emojis to engage the user.
    Do not provide any answers to queries that are not related to this website.
    If a query is related to this website and the documents do not contain sufficient data, you may generate relevant text. Ensure that any generated text is pertinent to the topic. Generate text to elaborate on topics if the available data in the documents is insufficient to provide a clear explanation.
    Website Home Page link: https://myousaf-codes.vercel.app/
    Website Tutorials Page link: https://myousaf-codes.vercel.app/tutorials
    Website About Page link: https://myousaf-codes.vercel.app/about
    Website Contact Page link: https://myousaf-codes.vercel.app/contact
    Website Blog Page link: https://myousaf-codes.vercel.app/blog

    Do not provide links in this format:

    - Link: https://myousaf-codes.vercel.app/blog/artificial-intelligence-conferences-malaysia-2025](https://myousaf-codes.vercel.app/blog/artificial-intelligence-conferences-malaysia-2025)
    Instead, use this format:

    - Link: https://myousaf-codes.vercel.app/blog/artificial-intelligence-conferences-malaysia-2025

    Do not include these elements in any links:

    - Brackets
    - Emojis

    - If the input is "by," "byby," "by by," "thank you," "goodbye," "good bye," "bye," "thank you," "thanks," "thank," "thank you so," or any similar farewell, the output should be a polite farewell such as, "Have a nice day," "Goodbye," or "Thank you."
    """,
    metadata={"source": "Instructions"},
)

document_10 = Document(
    page_content="""
    The developer of this website is Muhammad Yousuf.
    The developer of this chatbot is Muhammad Younus.
    The name of this website is MYousaf Codes.
    """,
    metadata={"source": "Introduction"},
)

document_11  = Document(
    page_content="""
    The developer of this website is Muhammad Yousuf.
    The developer of this chatbot is Muhammad Younus.
    The name of this website is MYousaf Codes.

    # 200 Questions
    questions = [
        "What is the main focus of MYousaf-Codes?",
        "What technologies does MYousaf-Codes specialize in?",
        "Can you list the frontend technologies used?",
        "What backend technologies are used by MYousaf-Codes?",
        "What database systems are used?",
        "Can you describe the Full-Stack CRM for ISP project?",
        "What technologies were used in the CRM project?",
        "What is the link to the About Us page?",
        "What is the link to the Tutorials page?",
        "What is the link to the Contact page?",
        "What services does MYousaf-Codes offer?",
        "How long does it take to complete a project?",
        "What is the payment structure?",
        "Does MYousaf-Codes provide ongoing maintenance and support?",
        "Who is Muhammad Yousuf?",
        "What is Muhammad Yousuf's primary role?",
        "What kind of developer is Muhammad Yousuf?",
        "Who is Muhammad Younus?",
        "Did Muhammad Younus develop the chatbot?",
        "What is the website's name?",
        "What does the tagline 'Building elegant solutions to complex problems' mean?",
        "What is the purpose of the Featured Projects section?",
        "How many projects are featured on the website?",
        "What is the purpose of the Skills & Expertise section?",
        "What is the difference between React and Next.js?",
        "What is Tailwind CSS used for?",
        "What is the difference between PostgreSQL and MongoDB?",
        "What is the role of Stripe in the projects?",
        "What is the role of Redux in the E-Commerce Platform?",
        "What is the purpose of the About Us page?",
        "How many projects has the team completed?",
        "What is the client satisfaction rate?",
        "How many team members are there?",
        "What companies has MYousaf-Codes worked with?",
        "What is the purpose of the tutorials section?",
        "What is the purpose of the contact section?",
        "How can I stay updated with the latest web development tips?",
        "What are the benefits of using TypeScript?",
        "What are the benefits of using Next.js?",
        "What is Muhammad Yousuf's experience in web development?",
        "How long has Muhammad Yousuf been a developer?",
        "What is Muhammad Yousuf's role in the 'About Us' section?",
        "Does Muhammad Yousuf contribute to the blog posts?",
        "Does Muhammad Yousuf work with international clients?",
        "Does Muhammad Yousuf handle project timelines and budgets?",
        "What is Muhammad Yousuf's expertise in frontend development?",
        "What is Muhammad Yousuf's expertise in backend development?",
        "What is Muhammad Yousuf's expertise in database and cloud technologies?",
        "Does Muhammad Yousuf contribute to open-source projects?",
        "How does Muhammad Yousuf stay updated with new technologies?",
        "Does Muhammad Yousuf work with React?",
        "Does Muhammad Yousuf work with Next.js?",
        "Does Muhammad Yousuf work with Python?",
        "Does Muhammad Yousuf work with TypeScript?",
        "Does Muhammad Yousuf work with AWS?",
        "Is Muhammad Yousuf involved in the design aspects of projects?",
        "Is Muhammad Yousuf involved in the testing phases of projects?",
        "Can Muhammad Yousuf integrate with existing development teams?",
        "Does Muhammad Yousuf provide post-launch support?",
        "How does Muhammad Yousuf ensure project quality?",
        "What is Muhammad Younus's area of expertise?",
        "Is Muhammad Younus involved in web development?",
        "What is Muhammad Younus's experience in AI?",
        "Is Muhammad Younus involved in any other projects on the website?",
        "How does Muhammad Younus approach chatbot development?",
        "Does Muhammad Younus use API keys in the chatbot?",
        "What is Muhammad Younus's background in Agentic AI?",
        "What is Muhammad Younus's approach to user interaction in the chatbot?",
        "How does Muhammad Younus ensure the chatbot is user-friendly?",
        "Does Muhammad Younus handle chatbot maintenance?",
        "What is the relationship between Muhammad Yousuf and Muhammad Younus?",
        "Do Muhammad Yousuf and Muhammad Younus work together on projects?",
        "Are Muhammad Yousuf and Muhammad Younus part of a larger team?",
        "Do Muhammad Yousuf and Muhammad Younus have similar skills?",
        "How do Muhammad Yousuf and Muhammad Younus communicate with clients?",
        "Do Muhammad Yousuf and Muhammad Younus contribute to the FAQ section?",
        "Are Muhammad Yousuf and Muhammad Younus involved in the blog content?",
        "What are the qualifications of Muhammad Yousuf and Muhammad Younus?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in website updates?",
        "How do Muhammad Yousuf and Muhammad Younus handle client feedback?",
        "Do Muhammad Yousuf and Muhammad Younus have any certifications?",
        "What is the educational background of Muhammad Yousuf and Muhammad Younus?",
        "How do Muhammad Yousuf and Muhammad Younus handle project communication?",
        "Are Muhammad Yousuf and Muhammad Younus involved in project planning?",
        "How do Muhammad Yousuf and Muhammad Younus ensure project security?",
        "What is the involvement of Muhammad Yousuf and Muhammad Younus in training new team members?",
        "Do Muhammad Yousuf and Muhammad Younus work with specific industries?",
        "What is the professional network of Muhammad Yousuf and Muhammad Younus?",
        "How do Muhammad Yousuf and Muhammad Younus handle project documentation?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in client consultations?",
        "Do Muhammad Yousuf and Muhammad Younus attend tech conferences?",
        "Do Muhammad Yousuf and Muhammad Younus contribute to tech communities?",
        "How do Muhammad Yousuf and Muhammad Younus handle project deadlines?",
        "What is the process of project handoff by Muhammad Yousuf and Muhammad Younus?",
        "Do Muhammad Yousuf and Muhammad Younus offer training or workshops?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's innovation?",
        "Do Muhammad Yousuf and Muhammad Younus have experience with startups?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in ensuring client satisfaction?",
        "Do Muhammad Yousuf and Muhammad Younus provide strategic digital solutions?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's growth?",
        "How do Muhammad Yousuf and Muhammad Younus approach problem-solving?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's mission?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's vision?",
        "Do Muhammad Yousuf and Muhammad Younus have any publications?",
        "How do Muhammad Yousuf and Muhammad Younus handle remote collaboration?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's success?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's user experience?",
        "Do Muhammad Yousuf and Muhammad Younus have experience in agile development?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's design?",
        "How do Muhammad Yousuf and Muhammad Younus ensure the website's accessibility?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's SEO?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's performance?",
        "Do Muhammad Yousuf and Muhammad Younus have experience with e-commerce platforms?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's security?",
        "How do Muhammad Yousuf and Muhammad Younus handle data privacy?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's content management?",
        "Do Muhammad Yousuf and Muhammad Younus have experience with API development?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's testing?",
        "How do Muhammad Yousuf and Muhammad Younus handle version control?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's deployment?",
        "What is the role of Muhammad Yousuf and Muhammad Younus in the website's maintenance and support?",
        "What is the purpose of the Full-Stack CRM for ISP project?",
        "What is the purpose of the Full-Stack E-Commerce Platform project?",
        "What is the link to the Full-Stack CRM for ISP project?",
        "What is the link to the Full-Stack E-Commerce Platform project?",
        "What technologies are used for building the server-rendered React application?",
        "What technologies are used to ensure type safety and enhance code quality?",
        "What technologies are used for efficient and responsive UI design?",
        "What is ShadCn UI used for?",
        "What is PostgreSQL?",
        "What is Auth.js used for in the projects?",
        "What is Stripe used for in the projects?",
        "What is Sanity?",
        "What is Redux used for?",
        "What is the purpose of listing the technologies used in the projects?",
        "What is the purpose of the Frontend Development category in Skills & Expertise?",
        "What is the purpose of the Backend Development category in Skills & Expertise?",
        "What is the purpose of the Database & Cloud category in Skills & Expertise?",
        "What is the purpose of the Additional Tools & Technologies category?",
        "What is Streamlit used for?",
        "What is FastAPI?",
        "What is Firebase?",
        "What is Supabase?",
        "What is Git used for?",
        "What is Docker used for?",
        "What is Webpack used for?",
        "What is REST APIs?",
        "What is Postman used for?",
        "What is VS Code?",
        "What is npm/yarn?",
        "What is the purpose of Figma?",
        "What is Vercel used for?",
        "How does the contact form use EmailJS?",
        "What are the benefits of using a collaborative development process?",
        "What is the purpose of automated testing and code reviews?",
        "What does 'agile methodology' mean in the context of development?",
        "How does the team ensure the application is robust, secure, and scalable?",
        "What does 'post-launch support' include?",
        "How does the team dedicate time to learning and exploring new technologies?",
        "What is the significance of participating in tech conferences?",
        "What does 'cross-industry insights' mean?",
        "What does 'transparency' mean in handling project budgets and timelines?",
        "What does 'real-time visibility into milestones' mean?",
        "What is the purpose of semantic markup in HTML5?",
        "What are accessibility best practices?",
        "What is SEO optimization?",
        "What is Flexbox and Grid in CSS?",
        "What are CSS variables?",
        "What is ES6+ in JavaScript?",
        "What is async/await in JavaScript?",
        "What are utility types in TypeScript?",
        "What are React Hooks?",
        "What is the Context API in React?",
        "What is SSR and SSG in Next.js?","What are RESTful APIs in Node.js?",
        "What is Django and Flask in Python?",
        "What is data analysis with pandas?",
        "What are automation scripts and web scraping techniques?",
        "What are React rendering issues and performance bottlenecks?",
        "What are CSS layout and responsive design problems?",
        "What are TypeScript type errors and compatibility issues?",
        "What are browser compatibility and polyfill solutions?",
        "What are Node.js memory leaks and performance optimization?",
        "What is API error handling and status code best practices?",
        "What is database connection and query optimization?",
        "What are authentication and security vulnerabilities?",
        "What is server vs. client component confusion in Next.js?",
        "What are data fetching and caching strategies in Next.js?",
        "What are routing and middleware complications in Next.js?",
        "What are deployment and build optimization in Next.js?",
        "What are Git merge conflicts and version control issues?",
        "What are package dependency conflicts and versioning?",
        "What are build and bundling configuration problems?",
        "What are testing and CI/CD pipeline troubleshooting?",
        "What is the link to the first blog about Artificial Intelligence Conferences in Malaysia 2025?",
        "What is the link to the second blog about Global Leaders Convene in Paris to Shape the Future of Artificial Intelligence?",
        "What is the content of the first blog?",
        "What is the content of the second blog?",
        "What is the purpose of the Artificial Intelligence Action Summit in Paris?",
        "What are the key outcomes of the Artificial Intelligence Action Summit?",
        "What is the International Declaration on AI Ethics and Safety?",
        "What is the European Union's 'InvestAI' initiative?",
        "What are the global implications of the Artificial Intelligence Action Summit?",
        "What is the conclusion of the second blog?",
        "Where can I find more updates and in-depth analyses on AI developments?",
        "What does MYousaf-Codes specialize in?",
        "What does MYousaf-Codes use database systems for?",
        "What does MYousaf-Codes emphasize in its tagline?",
        "What is the purpose of the 'Technologies We Work With' section?",
        "What does listing the technologies provide to visitors?",
        "What is the purpose of the 'Why Choose Us' section on the About Us page?",
        "What does 'Innovation First' mean as a reason to choose MYousaf-Codes?",
        "What does 'Customer Success' mean as a reason to choose MYousaf-Codes?",
        "What does 'Fast Delivery' mean as a reason to choose MYousaf-Codes?",
        "What does 'Growth Focused' mean as a reason to choose MYousaf-Codes?",
        "What is the purpose of the 'Meet Our Team' section?",
        "Who is Abdul Rauf?",
        "What are the credentials of the team?",
        "What is the purpose of the 'Why Partner With Us' section?",
        "What is the purpose of the 'Comprehensive Tutorials' section?",
        "What does the 'What You'll Learn' section cover?",
        "What does the 'Common Issues & Solutions' section provide?",
        "What is the purpose of the 'Stay Updated with Latest Web Development Tips' section?",
        "What information is included in the 'Contacts & Profiles' section?",
        "What is the purpose of the instructions in document_9?",
        "What are some examples of polite farewells the chatbot can use?",
        "Where can I find information about Full-Stack CRM for ISP?",
        "Where can I find information about Full-Stack E-Commerce Platform?",
        "What are the benefits of using Next.js for building server-rendered React applications?",
        "What are the benefits of using TypeScript to ensure type safety and enhance code quality?",
        "What are the benefits of using TailwindCSS for efficient and responsive UI design?",
        "What is the purpose of using ShadCn UI for consistent and reusable components?",
        "What is the purpose of using PostgreSQL as a powerful, open-source relational database system?",
        "What is the purpose of using Auth.js for implementing authentication and authorization features?",
        "What is the purpose of using Stripe to handle payment processing and subscription management?",
        "What is the purpose of using Sanity as a headless CMS for managing content?",
        "What is the purpose of using Redux for state management across the application?",
        "What are the benefits of using React for building user interfaces, particularly single-page applications?",
        "What are the benefits of using HTML5 as the standard markup language for creating web pages?",
        "What are the benefits of using CSS3 for styling web content?",
        "What are the benefits of using JavaScript as a versatile programming language essential for web development?",
        "What are the benefits of using Python for backend development?",
        "What are the benefits of using MongoDB as a NoSQL database known for its flexibility and scalability?",
        "What are the benefits of using Firebase as a platform developed by Google for creating mobile and web applications?",
        "What are the benefits of using Supabase as an open-source alternative to Firebase, offering backend services?",
        "What are the benefits of using Docker as a containerization platform?",
        "What are the benefits of using AWS as cloud computing services?",
        "What are the benefits of using Linux as an operating system?",
        "What are the benefits of using Postman as an API testing tool?",
        "What are the benefits of using VS Code as a code editor?",
        "What are the benefits of using Figma as a design tool?",
        "What are the benefits of using Vercel as a deployment platform?",
        "What is the purpose of using Git as a version control system?",
        "What is the purpose of using Webpack as a module bundler?",
        "What is the purpose of using GitHub Actions as a CI/CD tool?",
        "What are the benefits of using REST APIs as an architectural style for networked applications?",
        "What are the benefits of using npm/yarn as package managers?",
    ]

    """,
    metadata={"source": "Introduction"},
)

documents = [
    document_1,
    document_2,
    document_3,
    document_4,
    document_5,
    document_6,
    document_7,
    document_8,
    document_9,
    document_10,
    document_11
]

uuids = [str(uuid4()) for _ in range(len(documents))]
vector_store.add_documents(documents=documents, ids=uuids)

# Add LLM

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    tempreture=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# GET ANSWER

prompt_template = f"""
Your name is MYousuf-Codes Chatbot. You are here to help users with questions about the MYousaf-Codes website.

You MUST follow these rules:

1.  **Strictly adhere to the provided context:** ONLY answer questions using the information provided in the retrieved documents. Do NOT generate answers from your own knowledge.
2.  **Be formal and informative:** Provide clear and concise answers. Avoid conversational filler.
3.  **Acknowledge limitations:** If a question cannot be answered from the provided documents, respond with a polite message like: "I'm sorry, but I cannot answer that question based on the information available on the website."
4.  **Cite sources (where applicable):** If a specific piece of information comes from a particular document or section, mention it (e.g., "According to the About Us page...").
5.  **Provide links appropriately:** When providing links, ensure they are accurate and formatted correctly (e.g., "You can find more information on the Tutorials page: https://myousaf-codes.vercel.app/tutorials"). Do NOT use brackets or emojis in links.
6.  **Handle greetings and farewells:** Respond appropriately to greetings and farewells (e.g., "Hello!", "Goodbye!").
7. You have to answer these 200 questions by searching and reading all the documents and give answer according the informatoin given in other documents.:
    {document_11}
8. You don't have to answer the questions which are related to these topics:
General Knowledge

The history of the Roman Empire
The chemical composition of water
The theory of relativity
The plot of Shakespeare's "Hamlet"
The capitals of all countries in Africa
The highest mountain in South America
The causes of World War II
The process of photosynthesis
The life cycle of a butterfly
The different types of clouds
Current Events

The latest political developments in France
The current price of gold
Recent advancements in cancer research
The results of a specific sports game
Upcoming elections in Canada
The impact of climate change on the Arctic
Current economic trends in Japan
The latest news in the entertainment industry
Recent technological breakthroughs in renewable energy
International relations between specific countries
Science and Technology

The principles of quantum mechanics
How a car engine works
The human digestive system
The future of space exploration
The basics of genetic engineering
The technology behind virtual reality
The history of the internet
The development of artificial general intelligence
The concept of blockchain technology
The process of 3D printing
History and Culture

Ancient Egyptian mythology
The Renaissance period
The history of jazz music
Traditional Japanese art forms
The culture of indigenous tribes in Australia
The architecture of medieval castles
The history of the Olympic Games
The impact of the Industrial Revolution
The philosophy of existentialism
The art of Renaissance painters
Geography and Nature

The Amazon rainforest
The Great Barrier Reef
The formation of the Grand Canyon
The migration patterns of whales
The different types of biomes
The geology of volcanoes
The wildlife of the Serengeti
The water cycle
The solar system
The constellations
Food and Cooking

How to bake a soufflé
The origin of Italian cuisine
Different types of spices
The process of making wine
The art of sushi making
The chemistry of cooking
Vegan recipes
The history of chocolate
The effects of different diets
The science of taste
Hobbies and Recreation

How to play chess
The rules of cricket
The history of video games
Different types of martial arts
The art of photography
Techniques for learning a new language
The benefits of yoga
The hobby of bird watching
The craft of pottery
The skill of playing a musical instrument
Miscellaneous

The stock market
Legal systems
Fashion trends
Interior design
Car maintenance
Pet care
Gardening tips
Home improvement
Personal finance
Travel planning
Hypothetical Scenarios

What would happen if the moon disappeared?
The effects of time travel
The possibility of extraterrestrial life
The future of humanity
The ethics of cloning
The impact of artificial intelligence on society
The consequences of nuclear war
The feasibility of colonizing Mars
The existence of parallel universes
The nature of consciousness
Personal Opinions and Feelings

Your favorite movie
Your opinion on a specific political issue
Your feelings about a particular sports team
What you had for breakfast
Your personal beliefs
Your hobbies
Your favorite color
Your travel experiences
Your childhood memories
Your career aspirations

Here are the documents you can use to answer questions:
 [ f"""
document_1,
document_2,
document_3,
document_4,
document_5,
document_6,
document_7,
document_8,
document_9,
document_10,
"""]

You have to answer these 200 questions by searching and reading all the documents and give answer according the informatoin given in other documents.:
{document_11}
"""


while True:
  def answer_to_user(query: str):
    history = []

    vector_results = vector_store.similarity_search(query, k=2)
    history.append(f"role: User: {query}")

    final_answer = llm.invoke(f"""USER : {query},
    ChatBot : {vector_results}, {documents} """)
    history.append(f"role: ChatBot: {final_answer}")

    return final_answer

  if __name__ == "__main__":
    while True:
        user_query = input("Enter your query: ")
        model_response = answer_to_user(user_query)
        print(model_response.content)
        if user_query.lower() == "exit":
          break


# if __name__ == "__main__":
#   for question in questions:
#       response = answer_to_user(question)
#       print(f"**Question:** {question}")
#       print(f"**Answer:** {response.content}")
#       print("-" * 40)


## Command to run the chatbot: 
##
## python "C:\Users\Muhammad Yousuf\Desktop\Project\Agent\rag\mian.py"