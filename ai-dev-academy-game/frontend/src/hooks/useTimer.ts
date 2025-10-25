/**
 * useTimer - Custom hook for game timer
 */
import { useState, useEffect, useRef } from 'react';

export const useTimer = (initialTime: number = 0, autoStart: boolean = true) => {
  const [time, setTime] = useState(initialTime);
  const [isRunning, setIsRunning] = useState(autoStart);
  const intervalRef = useRef<number | null>(null);

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = window.setInterval(() => {
        setTime((prevTime) => prevTime + 0.1);
      }, 100);
    } else {
      if (intervalRef.current !== null) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current !== null) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning]);

  const start = () => setIsRunning(true);
  const pause = () => setIsRunning(false);
  const reset = () => {
    setTime(initialTime);
    setIsRunning(false);
  };

  return { time, isRunning, start, pause, reset };
};
