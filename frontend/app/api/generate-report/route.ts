import { NextRequest, NextResponse } from 'next/server';
import { v4 as uuidv4 } from 'uuid';
import { taskManager } from '@/lib/taskStore';
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

export async function POST(req: NextRequest) {
  const { description, model, apiKey } = await req.json();

  const taskId = uuidv4();
  
  console.log(`Creating new task: ${taskId}`);
  await taskManager.setTask(taskId, { status: 'processing', startTime: Date.now() });

  // Start the report generation process asynchronously
  generateReport(taskId, description, model, apiKey);

  console.log(`Returning response for task: ${taskId}`);
  return NextResponse.json({ taskId, status: 'processing' });
}

async function generateReport(taskId: string, description: string, model: string, apiKey: string) {
  try {
    console.log(`Starting report generation for task: ${taskId}`);
    
    const { stdout, stderr } = await execAsync(
      `python ../backend/generate_and_process_report.py "${description}" "${model}" "${apiKey}"`
    );
    
    console.log(`Raw stdout for task ${taskId}:`, stdout);
    
    if (stderr) {
      console.error(`Logs from generate_and_process_report.py for task ${taskId}:`, stderr);
    }

    try {
      const jsonStart = stdout.lastIndexOf('[');
      if (jsonStart === -1) {
        throw new Error('No JSON data found in output');
      }
      const jsonData = JSON.parse(stdout.slice(jsonStart));
      
      // Unescape the LaTeX expressions
      const unescapedData = jsonData.map((item: any) => {
        return Object.fromEntries(
          Object.entries(item).map(([key, value]) => [key, typeof value === 'string' ? value.replace(/\\\\/g, '\\') : value])
        );
      });

      console.log(`Report data generated for task: ${taskId}`);

      await taskManager.updateTaskStatus(taskId, 'completed', { data: unescapedData });
      console.log(`Task ${taskId} marked as completed`);
    } catch (parseError) {
      console.error(`Error parsing JSON output for task ${taskId}:`, parseError);
      throw new Error('Failed to parse report data');
    }
  } catch (error) {
    console.error(`Error in report generation for task ${taskId}:`, error);
    await taskManager.updateTaskStatus(taskId, 'failed', { error: error instanceof Error ? error.message : String(error) });
    console.log(`Task ${taskId} marked as failed`);
  }
}
