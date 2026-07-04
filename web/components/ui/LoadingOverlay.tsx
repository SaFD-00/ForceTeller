'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { Icon } from './Icon';

interface LoadingOverlayProps {
  isVisible: boolean;
  message?: string;
  subMessage?: string;
}

export function LoadingOverlay({
  isVisible,
  message = '사주를 분석하고 있습니다',
  subMessage = '잠시만 기다려주세요...',
}: LoadingOverlayProps) {
  return (
    <AnimatePresence>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.3 }}
          className="fixed inset-0 z-50 flex items-center justify-center bg-background/95 backdrop-blur-xl"
        >
          <div className="text-center">
            {/* Animated circles */}
            <div className="relative w-32 h-32 mx-auto mb-8">
              {/* Outer rotating ring */}
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-0 rounded-full border-2 border-transparent border-t-primary border-r-primary/50"
              />

              {/* Middle rotating ring (opposite direction) */}
              <motion.div
                animate={{ rotate: -360 }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                className="absolute inset-2 rounded-full border-2 border-transparent border-b-accent border-l-accent/50"
              />

              {/* Inner pulsing circle */}
              <motion.div
                animate={{ scale: [1, 1.1, 1], opacity: [0.5, 1, 0.5] }}
                transition={{ duration: 1.5, repeat: Infinity, ease: 'easeInOut' }}
                className="absolute inset-4 rounded-full bg-gradient-to-br from-primary/20 to-accent/20 flex items-center justify-center"
              >
                <Icon
                  name="solar:stars-bold"
                  size={40}
                  className="text-primary"
                />
              </motion.div>
            </div>

            {/* Text */}
            <motion.h2
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="text-2xl font-bold text-foreground mb-2"
            >
              {message}
            </motion.h2>

            <motion.p
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="text-muted-foreground"
            >
              {subMessage}
            </motion.p>

            {/* Animated dots */}
            <div className="flex justify-center gap-2 mt-6">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  animate={{
                    y: [0, -8, 0],
                    opacity: [0.3, 1, 0.3],
                  }}
                  transition={{
                    duration: 0.8,
                    repeat: Infinity,
                    delay: i * 0.15,
                  }}
                  className="w-2 h-2 rounded-full bg-primary"
                />
              ))}
            </div>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
