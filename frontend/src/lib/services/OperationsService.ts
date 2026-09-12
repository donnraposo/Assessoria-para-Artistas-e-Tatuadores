import { ApiClient } from "../http/ApiClient";
import type { ArtistApplicationQueueItem } from "../types/artist";
import type { OperationsDashboard, QueuePage, RoleWorkspace } from "../types/operations";

export class OperationsService {
  static dashboard(): Promise<OperationsDashboard> {
    return ApiClient.get<OperationsDashboard>("/operations/dashboard/");
  }

  static roleWorkspace(): Promise<RoleWorkspace> {
    return ApiClient.get<RoleWorkspace>("/operations/workspace/");
  }

  static artistApplicationQueue(page: number): Promise<QueuePage<ArtistApplicationQueueItem>> {
    return ApiClient.get<QueuePage<ArtistApplicationQueueItem>>(
      `/operations/queues/artist-applications/?page=${page}`,
    );
  }
}
