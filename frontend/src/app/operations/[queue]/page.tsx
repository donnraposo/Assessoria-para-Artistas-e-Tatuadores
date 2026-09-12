import { OperationsQueueScreen } from "@/components/OperationsQueueScreen";

type OperationsQueuePageProps = { params: Promise<{ queue: string }> };

export default async function OperationsQueuePage({ params }: OperationsQueuePageProps) {
  const { queue } = await params;
  return <OperationsQueueScreen queueSlug={queue} />;
}
