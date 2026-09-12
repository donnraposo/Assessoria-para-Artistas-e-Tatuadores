type LoadingScreenProps = {
  message: string;
};

export function LoadingScreen({ message }: LoadingScreenProps) {
  return (
    <main aria-busy="true" className="centered-state">
      <span className="loader" />
      <p role="status">{message}</p>
    </main>
  );
}
