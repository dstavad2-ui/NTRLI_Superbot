#!/bin/bash

###############################################################################
# NTRLI SuperAPK - Complete Setup & Build Script
# Phone-only execution - No PC required
###############################################################################

set -e

echo "====================================="
echo "NTRLI SuperAPK Build System"
echo "====================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
APP_DIR="app1"
BUILD_DIR="$APP_DIR/.buildozer"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v $1 &> /dev/null; then
        log_error "$1 not found. Please install it first."
        return 1
    fi
    log_info "$1 is installed"
    return 0
}

clean_build() {
    log_info "Cleaning previous build..."
    rm -rf ~/.buildozer
    rm -rf $BUILD_DIR
    log_info "Build environment cleaned"
}

create_directories() {
    log_info "Creating directory structure..."
    mkdir -p $APP_DIR/modules
    mkdir -p $APP_DIR/assets
    log_info "Directories created"
}

create_assets() {
    log_info "Creating placeholder assets..."
    
    # Create icon (64x64 red square as placeholder)
    cat > $APP_DIR/assets/icon.png << 'EOF'
iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAD3SURBVHic7doxCoAwDIBRxf4n7eLg7OIg7uDiICq4iCKCBzCLi4PLwU1w8QLSDi0kJPCGyBt6EQghhBBCCCGEEEIIIYQQQgghhBBCCPkdABwBVABq/gPgCqABkP8AuAFoAeQ/AG4AGgDlD4AGgAZA+QOgBaABUP4AaAFoAJQ/AFoAGgDlD4AWgAZA+QOgBaABUP4AaAFoAJQ/AFoAGgDlD4AWgAZA+QOgBaABUP4AaAFoAJQ/AFoAGgDlD4AWgAZA+QOgBaABUP4AaAFoAJQ/AFoAGgDlD4AWgAZA+QOgBaABUP4AaAFoAJQ/AFoAGgDlD4AWAAAAAL8FgA8AAP//AwBKhwAAAAAAAElFTkSuQmCC
EOF

    log_info "Assets created"
}

phase0_setup() {
    log_info "========== PHASE 0: MINIMAL STABLE =========="
    
    # Check dependencies
    check_command python3 || exit 1
    check_command pip3 || exit 1
    
    log_info "Installing Phase 0 dependencies..."
    pip3 install --user kivy==2.3.1 kivymd==1.1.1
    
    log_info "Phase 0 setup complete"
}

phase1_setup() {
    log_info "========== PHASE 1: AUTH & NETWORK =========="
    
    log_info "Installing Phase 1 dependencies..."
    pip3 install --user requests==2.31.0 pysocks==1.7.1 cryptography==41.0.7
    
    # Update buildozer.spec with Phase 1 requirements
    sed -i 's/requirements = python3==3.11.8,kivy==2.3.1,kivymd==1.1.1/requirements = python3==3.11.8,kivy==2.3.1,kivymd==1.1.1,requests==2.31.0,pysocks==1.7.1,cryptography==41.0.7/' $APP_DIR/buildozer.spec
    
    log_info "Phase 1 setup complete"
}

phase2_setup() {
    log_info "========== PHASE 2: NEWS & ECOMMERCE =========="
    
    log_info "Installing Phase 2 dependencies..."
    pip3 install --user feedparser==6.0.10 pillow==10.2.0 sqlalchemy==2.0.25
    
    # Update buildozer.spec
    sed -i 's/cryptography==41.0.7/cryptography==41.0.7,feedparser==6.0.10,pillow==10.2.0,sqlalchemy==2.0.25/' $APP_DIR/buildozer.spec
    
    # Add POST_NOTIFICATIONS permission
    sed -i 's/READ_EXTERNAL_STORAGE/READ_EXTERNAL_STORAGE,POST_NOTIFICATIONS/' $APP_DIR/buildozer.spec
    
    log_info "Phase 2 setup complete"
}

phase3_setup() {
    log_info "========== PHASE 3: AI & ADMIN =========="
    
    log_info "Installing Phase 3 dependencies..."
    pip3 install --user flask==3.0.2 anthropic==0.18.0 openai==1.12.0 babel==2.14.0
    
    # Update buildozer.spec
    sed -i 's/sqlalchemy==2.0.25/sqlalchemy==2.0.25,flask==3.0.2,anthropic==0.18.0,openai==1.12.0,babel==2.14.0/' $APP_DIR/buildozer.spec
    
    log_info "Phase 3 setup complete"
}

build_apk() {
    log_info "========== BUILDING APK =========="
    
    cd $APP_DIR
    
    if ! command -v buildozer &> /dev/null; then
        log_warn "Buildozer not found. Installing..."
        pip3 install --user buildozer
    fi
    
    log_info "Starting Buildozer build..."
    buildozer android debug
    
    if [ $? -eq 0 ]; then
        log_info "Build successful!"
        log_info "APK location: $APP_DIR/bin/*.apk"
    else
        log_error "Build failed. Check logs above."
        exit 1
    fi
    
    cd ..
}

run_tests() {
    log_info "========== RUNNING TESTS =========="
    
    log_info "Checking crash log..."
    if [ -f "/sdcard/superbot_crash.log" ]; then
        log_info "Crash log exists"
        tail -n 20 /sdcard/superbot_crash.log
    else
        log_info "No crash log found (good!)"
    fi
    
    log_info "Checking AI console logs..."
    if [ -f "/sdcard/AI_consoles_main.log" ]; then
        log_info "AI console log exists"
        tail -n 20 /sdcard/AI_consoles_main.log
    else
        log_warn "No AI console log found"
    fi
}

# Main execution
main() {
    echo ""
    log_info "Starting SuperAPK build process..."
    echo ""
    
    # Parse command line arguments
    PHASE="all"
    if [ $# -gt 0 ]; then
        PHASE=$1
    fi
    
    case $PHASE in
        clean)
            clean_build
            ;;
        0|phase0)
            create_directories
            create_assets
            phase0_setup
            ;;
        1|phase1)
            phase1_setup
            ;;
        2|phase2)
            phase2_setup
            ;;
        3|phase3)
            phase3_setup
            ;;
        build)
            build_apk
            ;;
        test)
            run_tests
            ;;
        all)
            clean_build
            create_directories
            create_assets
            phase0_setup
            log_warn "Phase 0 complete. Test the app before proceeding to Phase 1."
            log_info "To continue: ./setup.sh 1"
            ;;
        *)
            echo "Usage: $0 [clean|0|1|2|3|build|test|all]"
            echo ""
            echo "  clean    - Clean build environment"
            echo "  0/phase0 - Setup Phase 0 (minimal stable)"
            echo "  1/phase1 - Setup Phase 1 (auth & network)"
            echo "  2/phase2 - Setup Phase 2 (news & ecommerce)"
            echo "  3/phase3 - Setup Phase 3 (AI & admin)"
            echo "  build    - Build APK"
            echo "  test     - Run tests and check logs"
            echo "  all      - Run Phase 0 setup"
            exit 1
            ;;
    esac
    
    echo ""
    log_info "Operation complete!"
    echo ""
}

main "$@"