This is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## New Capabilities

The app now includes agents for business idea evaluation, market research, revenue model, MVP features, investment strategy, go-to-market strategy, scaling, competitor analysis, pivot ideas, target audience profiling, risk assessment, legal compliance, and business model canvas generation. These agents are structured using `System`, `Instruction`, `GraphExecutor`, and `InstructionMapEngine` from the `lionagi` library.

## New Agents and Their Roles

1. **Business Idea Evaluation**: Evaluates the given business idea, assessing its viability, potential, and uniqueness in the market. Identifies key strengths, weaknesses, opportunities, and threats.
2. **Market Research**: Conducts a comprehensive market analysis for the given business idea. Determines the Total Addressable Market (TAM), Serviceable Addressable Market (SAM), and Serviceable Obtainable Market (SOM). Identifies key market trends, growth potential, and competitive landscape.
3. **Revenue Model**: Suggests suitable revenue models for the given business idea. Considers the target market, industry dynamics, and potential scalability. Recommends the most appropriate model(s), providing pros and cons for each. Estimates potential revenue streams and explains how they align with the business goals.
4. **MVP Features**: Proposes suitable Minimum Viable Product (MVP) features for the given business idea. Focuses on core functionalities that demonstrate value and address the main problem. Prioritizes features based on development time and impact. Suggests a timeline for MVP development and recommends metrics to measure its success.
5. **Investment Strategy**: Creates a compelling investor pitch template for the given business idea. Develops a clear and concise value proposition. Outlines the problem, solution, and market opportunity. Highlights the team's expertise and competitive advantage. Includes key financial projections and funding requirements. Ensures the pitch is tailored to attract potential investors.
6. **Go-to-Market Strategy**: Devises effective strategies for the given business idea. Identifies target customer segments and recommends appropriate marketing channels. Suggests pricing strategies and develops a comprehensive customer acquisition plan. Considers the target audience, market conditions, and available resources to create a tailored approach.
7. **Scaling**: Provides guidance on raising funds for the startup. Explains different funding sources (e.g., VC, angel investors, crowdfunding) and recommends the most suitable options for the current business stage. Provides tips for successful fundraising pitches and advises on equity dilution and valuation considerations.
8. **Competitor Analysis**: Conducts a thorough analysis of direct and indirect competitors for the given business idea. Identifies key players, analyzes their strengths and weaknesses, and compares features, pricing, and market positioning. Highlights competitive advantages and disadvantages, and suggests strategies to differentiate from competitors.
9. **Pivot Ideas**: Generates alternative ideas and pivot options related to the original business concept. Suggests related business ideas in the same industry and proposes pivot options that leverage existing resources. Identifies potential new markets or customer segments and evaluates the feasibility of each pivot option.
10. **Target Audience Profiling**: Identifies and profiles the initial target audience for the given business idea. Conducts primary and secondary research to identify target demographics, create detailed customer personas, analyze customer needs, preferences, and behaviors. Recommends strategies to reach and engage the target audience effectively.
11. **Risk Assessment**: Assesses potential risks associated with the business idea and provides strategies to mitigate them. Considers market, financial, operational, and legal risks.
12. **Legal Compliance**: Ensures that the business idea complies with relevant laws and regulations. Provides guidance on legal requirements and best practices.
13. **Business Model Canvas Generation**: Generates a comprehensive business model canvas for the given business idea. Identifies key partners, activities, resources, value propositions, customer relationships, channels, customer segments, cost structure, and revenue streams.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.
