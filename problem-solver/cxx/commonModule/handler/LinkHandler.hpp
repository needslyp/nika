#include <string>
#include <vector>

#include "sc-memory/sc_memory.hpp"

namespace commonModule
{
class LinkHandler
{
public:
  explicit LinkHandler(ScMemoryContext * context);

  ScAddr createLink(const std::string & text);

private:
  ScMemoryContext * context;
};
}

