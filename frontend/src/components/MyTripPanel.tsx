import type { MyTrip } from "@/lib/api";
import { formatCurrency } from "@/lib/format";

import { Icon } from "./Icon";
import { StatusBadge } from "./StatusBadge";

type MyTripPanelProps = { trip: MyTrip };

export function MyTripPanel({ trip }: MyTripPanelProps) {
  return (
    <section className="trip-panel">
      <div className="section-heading">
        <div>
          <h3>My Trip · {trip.guest.city}</h3>
          <p>Everything the agency arranged for this Guest.</p>
        </div>
        <div className="trip-summary">
          <StatusBadge status={trip.status} />
          <strong>{formatCurrency(trip.costs.total, trip.costs.currency)}</strong>
          <small>Total cost you cover</small>
        </div>
      </div>
      <div className="trip-grid">
        <div>
          <h4><Icon name="trip" />Travel</h4>
          {trip.travel_segments.length === 0
            ? <p>Travel details are pending.</p>
            : trip.travel_segments.map((segment) => (
              <article key={segment.id}>
                <strong>{segment.origin} → {segment.destination}</strong>
                <span>{new Date(segment.departs_at).toLocaleString("en-US")}</span>
              </article>
            ))}
        </div>
        <div>
          <h4><Icon name="studio" />Accommodation</h4>
          {trip.accommodations.length === 0
            ? <p>Accommodation details are pending.</p>
            : trip.accommodations.map((item) => (
              <article key={item.id}><strong>{item.name}</strong><span>{item.address}</span></article>
            ))}
        </div>
        <div>
          <h4><Icon name="reservation" />Studios</h4>
          {trip.studios.length === 0
            ? <p>No Studio assigned.</p>
            : trip.studios.map((item) => (
              <article key={item.id}><strong>{item.studio_name}</strong><span>{item.studio_address}</span></article>
            ))}
        </div>
        <div>
          <h4><Icon name="schedule" />Appointments</h4>
          {trip.appointments.length === 0
            ? <p>No appointments yet.</p>
            : trip.appointments.map((item) => (
              <article key={item.id}>
                <strong>{item.studio_name}</strong>
                <span>{new Date(item.starts_at).toLocaleString("en-US")}</span>
              </article>
            ))}
        </div>
      </div>
    </section>
  );
}
