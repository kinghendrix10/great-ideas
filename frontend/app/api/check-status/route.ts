import { NextRequest, NextResponse } from 'next/server';
import { taskManager } from '@/lib/taskStore';

export async function GET(req: NextRequest) {
  const taskId = req.nextUrl.searchParams.get('taskId');

  console.log(`Checking status for task: ${taskId}`);

  if (!taskId) {
    console.log('Missing taskId');
    return NextResponse.json({ error: 'Missing taskId' }, { status: 400 });
  }

  const task = await taskManager.getTask(taskId);

  if (!task) {
    console.log(`Task not found: ${taskId}`);
    return NextResponse.json({ error: 'Task not found' }, { status: 404 });
  }

  console.log(`Returning status for task: ${taskId}`, task);
  return NextResponse.json({ status: task.status, pdfPath: task.pdfPath });
}
