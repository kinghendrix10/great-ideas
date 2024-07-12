import { NextRequest, NextResponse } from 'next/server';
import { taskManager } from '@/lib/taskStore';
import { readFile } from 'fs/promises';
import path from 'path';

export async function GET(req: NextRequest) {
  const taskId = req.nextUrl.searchParams.get('taskId');

  if (!taskId) {
    return NextResponse.json({ error: 'Missing taskId' }, { status: 400 });
  }

  const task = await taskManager.getTask(taskId);

  if (!task || task.status !== 'completed') {
    return NextResponse.json({ error: 'Report not ready' }, { status: 404 });
  }

  try {
    const pdfPath = path.join(process.cwd(), 'public', `report_${taskId}.pdf`);
    const pdfBuffer = await readFile(pdfPath);

    return new NextResponse(pdfBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'application/pdf',
        'Content-Disposition': `attachment; filename=business_report_${taskId}.pdf`,
      },
    });
  } catch (error) {
    console.error('Error reading PDF file:', error);
    return NextResponse.json({ error: 'Error reading PDF file' }, { status: 500 });
  }
}
